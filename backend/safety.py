UNSAFE_KEYWORDS = [
    "pregnant", "pregnancy", "trimester",
    "hernia", "glaucoma",
    "high blood pressure", "bp",
    "recent surgery", "post surgery",
    "knee injury", "back injury",
    "heart condition"
]

def is_unsafe(query: str) -> bool:
    q = query.lower()
    return any(keyword in q for keyword in UNSAFE_KEYWORDS)
