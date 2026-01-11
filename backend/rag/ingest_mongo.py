import json
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import pdfplumber

# ---------------- CONFIG ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

client = MongoClient("mongodb://localhost:27017")
db = client["yogaRAG"]
chunks_col = db["chunks"]

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "vectorstore"

# Load ALL JSON files automatically
JSON_FILES = list(DATA_DIR.glob("*.json"))

# PDF FILES
PDF_PATHS = [
    DATA_DIR / "30 Essential Yoga Poses _ for beginning students and their teachers.pdf",
    DATA_DIR / "HealthFitness_YOGA_Manual.pdf"
]

# ---------------- NORMALIZATION ----------------

def normalize_pose_names(text: str) -> str:
    replacements = {
        "śavāsana": "shavasana",
        "savasana": "shavasana",
        "corpse pose": "shavasana",
        "corpse posture": "shavasana",
        "vajrāsana": "vajrasana"
    }
    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# ---------------- CHUNKING ----------------

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk) > 200:
            chunks.append(chunk)
    return chunks

def ingest_text(title, source, text):
    docs = []
    text = normalize_pose_names(text)
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = model.encode(chunk).tolist()
        docs.append({
            "title": title,
            "source": source,
            "content": chunk,
            "embedding": embedding,
            "createdAt": datetime.utcnow()
        })
    return docs

# ---------------- JSON HELPERS ----------------

def dict_to_text(d: dict) -> str:
    lines = []
    for k, v in d.items():
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        lines.append(f"{k.replace('_', ' ').title()}: {v}")
    return "\n".join(lines)

# ---------------- INGEST ----------------

docs = []

# ---- INGEST ALL JSON FILES ----
print(f"📘 Loading {len(JSON_FILES)} JSON files...")

for json_path in JSON_FILES:
    print(f"➡️ Processing {json_path.name}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Case 1: List of articles
    if isinstance(data, list):
        for item in data:
            text = dict_to_text(item)
            docs.extend(
                ingest_text(
                    title=item.get("title", json_path.stem),
                    source=json_path.name,
                    text=text
                )
            )

    # Case 2: Detailed asanas (has "asanas")
    elif isinstance(data, dict) and "asanas" in data:
        for asana in data["asanas"]:
            text = dict_to_text(asana)
            docs.extend(
                ingest_text(
                    title=asana.get("english_name", "Yoga Asana"),
                    source=json_path.name,
                    text=text
                )
            )

    # Case 3: Category-based asanas or generic dict JSON
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    text = dict_to_text(item)
                    docs.extend(
                        ingest_text(
                            title=item.get("english", key),
                            source=json_path.name,
                            text=text
                        )
                    )

# ---- INGEST PDFs ----
print("📄 Loading PDFs...")

for pdf_path in PDF_PATHS:
    if not pdf_path.exists():
        continue

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text or len(text) < 300:
                continue

            docs.extend(
                ingest_text(
                    title=f"{pdf_path.stem} – page {i+1}",
                    source=pdf_path.name,
                    text=text
                )
            )

# ---- STORE IN MONGODB ----
print("🗑️ Clearing old chunks...")
chunks_col.delete_many({})

print(f"📥 Inserting {len(docs)} chunks into MongoDB...")
chunks_col.insert_many(docs)

print("✅ MongoDB vector store ready (ALL JSONs unified)")
