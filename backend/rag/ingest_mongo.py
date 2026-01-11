import json
from pathlib import Path
from datetime import datetime, timezone
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# ---------------- CONFIG ----------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

client = MongoClient("mongodb://localhost:27017")
db = client["yogaRAG"]
chunks_col = db["chunks"]

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "vectorstore"

# Load ALL JSON files
JSON_FILES = list(DATA_DIR.glob("*.json"))

# ---------------- CHUNKING ----------------

def chunk_text(text, chunk_size=400, overlap=50):
    """
    Used ONLY for long documents (articles, asana descriptions).
    Q&A data bypasses this.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 200:
            chunks.append(chunk)
    return chunks

# ---------------- EMBEDDING ----------------

def embed_text(text: str):
    """
    Returns a normalized 384-dim float32 embedding (cosine-ready)
    """
    emb = model.encode(text, normalize_embeddings=True)
    emb = np.asarray(emb, dtype=np.float32)

    if emb.shape[0] != EMBEDDING_DIMENSION:
        raise ValueError(f"Embedding dimension mismatch: {emb.shape[0]}")

    return emb.tolist()

# ---------------- INGEST CORE ----------------

def ingest_text(title, source, text, doc_type):
    """
    doc_type: qa | asana | article
    """
    docs = []

    # 🔥 CRITICAL FIX
    if doc_type == "qa":
        # Store Q&A as a SINGLE chunk (never drop it)
        chunks = [text]
    else:
        chunks = chunk_text(text)

    for chunk in chunks:
        docs.append({
            "title": title,
            "source": source,
            "doc_type": doc_type,            # 🔥 IMPORTANT FOR DEBUGGING
            "content": chunk,
            "embedding": embed_text(chunk),
            "createdAt": datetime.now(timezone.utc)
        })

    return docs

# ---------------- JSON HELPERS ----------------

def dict_to_text(d: dict) -> str:
    """
    Converts JSON object into readable text for embedding
    """
    lines = []
    for k, v in d.items():
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        lines.append(f"{k.replace('_', ' ').title()}: {v}")
    return "\n".join(lines)

# ---------------- INGEST ----------------

docs = []

print(f"📘 Loading {len(JSON_FILES)} JSON files...")

for json_path in JSON_FILES:
    print(f"➡️ Processing {json_path.name}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- CASE 1: Q&A FILES ----------
    if (
        isinstance(data, list)
        and len(data) > 0
        and all("question" in x and "answer" in x for x in data)
    ):
        for item in data:
            text = f"Question: {item['question']}\nAnswer: {item['answer']}"
            docs.extend(
                ingest_text(
                    title=item["question"],
                    source=json_path.name,
                    text=text,
                    doc_type="qa"
                )
            )

    # ---------- CASE 2: DETAILED ASANAS ----------
    elif isinstance(data, dict) and "asanas" in data:
        for asana in data["asanas"]:
            text = dict_to_text(asana)
            docs.extend(
                ingest_text(
                    title=asana.get("english_name", asana.get("asana", "Yoga Asana")),
                    source=json_path.name,
                    text=text,
                    doc_type="asana"
                )
            )

    # ---------- CASE 3: ARTICLES / GENERIC LIST ----------
    elif isinstance(data, list):
        for item in data:
            text = dict_to_text(item)
            docs.extend(
                ingest_text(
                    title=item.get("title", json_path.stem),
                    source=json_path.name,
                    text=text,
                    doc_type="article"
                )
            )

    # ---------- CASE 4: CATEGORY-BASED JSON ----------
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    text = dict_to_text(item)
                    docs.extend(
                        ingest_text(
                            title=item.get("english", key),
                            source=json_path.name,
                            text=text,
                            doc_type="asana"
                        )
                    )

# ---------------- MONGODB ----------------

print("🗑️ Clearing old chunks...")
chunks_col.delete_many({})

print(f"📥 Inserting {len(docs)} chunks into MongoDB...")
chunks_col.insert_many(docs)

print("✅ MongoDB vector store ready")
print("   ✔ Q&A preserved")
print("   ✔ 384-dim embeddings")
print("   ✔ Cosine similarity ready")
