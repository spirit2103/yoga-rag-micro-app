import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = MongoClient("mongodb://localhost:27017")
db = client["yogaRAG"]
chunks_col = db["chunks"]

POSE_SYNONYMS = {
    "vajrasana": ["vajrasana"],
    "shavasana": ["shavasana"]
}

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=3):
    query_emb = model.encode(query)
    min_score = 0.60 if len(query.split()) <= 5 else 0.75
    results = []

    for doc in chunks_col.find({}, {
        "_id": 0,
        "title": 1,
        "source": 1,
        "content": 1,
        "embedding": 1
    }):
        score = cosine_similarity(query_emb, np.array(doc["embedding"]))
        if score >= min_score:
            results.append({
                "title": doc["title"],
                "source": doc["source"],
                "content": doc["content"],
                "score": float(score)
            })

    results.sort(key=lambda x: x["score"], reverse=True)

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
