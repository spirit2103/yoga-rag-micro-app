def build_prompt(query, contexts):
    context_text = "\n\n".join(
        f"[Source: {c.get('title', 'Unknown')} – {c.get('source', 'local')}]\n"
        f"{c.get('content', '')}"
        for c in contexts
        if c.get("content")
    )

    return f"""
You are a yoga assistant.

Use ALL the information below to answer the question.
You may combine and summarize across sources.
Do not use any knowledge outside the context.

Context:
{context_text}

Question:
{query}

Answer:
"""
