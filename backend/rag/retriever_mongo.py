import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

client = MongoClient("mongodb://localhost:27017")
db = client["yogaRAG"]
chunks_col = db["chunks"]

POSE_SYNONYMS = {
    "vajrasana": ["vajrasana"],
    "shavasana": ["shavasana", "corpse pose"]
}

# ---------------- COSINE SIMILARITY ----------------

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity for normalized float32 vectors
    """
    return float(np.dot(a, b))

# ---------------- EMBEDDING ----------------

def embed_query(text: str) -> np.ndarray:
    """
    Returns a normalized 384-dim float32 embedding
    """
    emb = model.encode(text, normalize_embeddings=True)
    emb = np.asarray(emb, dtype=np.float32)

    assert emb.shape[0] == EMBEDDING_DIMENSION, \
        f"Embedding dimension mismatch: {emb.shape[0]}"

    return emb

# ---------------- RETRIEVER ----------------

def retrieve(query: str, top_k: int = 3):
    query_emb = embed_query(query)

    # Dynamic threshold based on query length
    min_score = 0.60 if len(query.split()) <= 5 else 0.75

    results = []

    for doc in chunks_col.find(
        {},
        {
            "_id": 0,
            "title": 1,
            "source": 1,
            "content": 1,
            "embedding": 1
        }
    ):
        doc_emb = np.asarray(doc["embedding"], dtype=np.float32)

        # Safety check
        if doc_emb.shape[0] != EMBEDDING_DIMENSION:
            continue

        score = cosine_similarity(query_emb, doc_emb)

        if score >= min_score:
            results.append({
                "title": doc["title"],
                "source": doc["source"],
                "content": doc["content"],
                "score": score
            })

    # Sort by cosine similarity
    results.sort(key=lambda x: x["score"], reverse=True)

    # ---------------- POSE FILTERING ----------------

    query_lower = query.lower()

    for pose, keywords in POSE_SYNONYMS.items():
        if pose in query_lower:
            filtered = [
                r for r in results
                if any(k in r["content"] for k in keywords)
            ]
            if filtered:
                results = filtered

    return results[:top_k]
