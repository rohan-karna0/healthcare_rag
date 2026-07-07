def add_context_prefix(chunks: list[str], title: str, source: str) -> list[str]:
    prefix = f"Source: {source} | Title: {title}\n"
    return [f"{prefix}{chunk}" for chunk in chunks]
