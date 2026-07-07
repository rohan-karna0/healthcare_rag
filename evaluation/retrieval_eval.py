EVAL_QUESTIONS = [
    {
        "question": "What is type 2 diabetes?",
        "expected_sources": ["CDC", "WHO"],
        "keywords": ["type 2", "insulin", "adults"],
    },
  {
    "question": "What are symptoms of diabetes?",
    "expected_sources": ["CDC", "WHO"],
    "keywords": ["thirst", "urination", "hunger"],
  },
]


def precision_at_k(retrieved_sources: list[str], expected_sources: list[str], k: int = 5) -> float:
    top = retrieved_sources[:k]
    if not top:
        return 0.0
    hits = sum(1 for source in top if source in expected_sources)
    return hits / len(top)
