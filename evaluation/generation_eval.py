def keyword_overlap(answer: str, keywords: list[str]) -> float:
    answer_lower = answer.lower()
    if not keywords:
        return 0.0
    hits = sum(1 for keyword in keywords if keyword.lower() in answer_lower)
    return hits / len(keywords)
