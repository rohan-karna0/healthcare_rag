HEALTHCARE_EXPANSIONS = {
    "diabetes": ["blood sugar", "glucose", "insulin", "hyperglycemia"],
    "hypertension": ["high blood pressure", "bp"],
    "heart": ["cardiac", "cardiovascular"],
    "cancer": ["oncology", "tumor", "malignancy"],
}


def expand_query(query: str) -> str:
    terms = query.lower().split()
    extras: list[str] = []
    for term in terms:
        extras.extend(HEALTHCARE_EXPANSIONS.get(term, []))
    if not extras:
        return query
    return f"{query} {' '.join(sorted(set(extras)))}"
