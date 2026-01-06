CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "self harm",
    "hurt myself",
    "i want to die"
]

def detect_crisis(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in CRISIS_KEYWORDS)
