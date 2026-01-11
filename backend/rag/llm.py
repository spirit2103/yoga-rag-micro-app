import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-120b"

def generate_answer(query, contexts):
    if not contexts:
        return "The retrieved sources do not provide enough information to answer this question."

    context_text = "\n\n".join(c["content"] for c in contexts)

    prompt = f"""
You are a yoga assistant.

Answer ONLY using the context below.
Every point must be supported by the context.
Do NOT introduce other yoga poses.
If the answer is not present, say so.

Use numbered points.
Max 5 points. Max 100 words.
No markdown or special symbols.

Context:
{context_text}

Question:
{query}

Answer:
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content.strip()
