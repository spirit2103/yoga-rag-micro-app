from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from rag.retriever_mongo import retrieve
from rag.llm import generate_answer
from safety import is_unsafe
from db import queries_collection

app = FastAPI(title="Yoga RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"status": "Yoga RAG backend running"}

@app.post("/ask")
def ask(req: AskRequest):
    query = req.query.strip()

    unsafe = is_unsafe(query)
    retrieved_chunks = retrieve(query, top_k=4)

    sources = [
        f"{c['title']} – {c['source']}"
        for c in retrieved_chunks
    ]

    if unsafe:
        answer = (
            "Your question touches on an area that can be risky without personalized guidance. "
            "Please consult a doctor or certified yoga therapist before attempting any practices."
        )
    else:
        if not retrieved_chunks:
            answer = "I do not have enough information to answer this question."
        else:
            answer = generate_answer(query, retrieved_chunks)

    queries_collection.insert_one({
        "query": query,
        "sources": sources,
        "answer": answer,
        "isUnsafe": unsafe,
        "timestamp": datetime.utcnow()
    })

    return {
        "answer": answer,
        "sources": sources,
        "isUnsafe": unsafe,
        "warning": "Consult a professional" if unsafe else ""
    }
