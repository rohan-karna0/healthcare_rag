import re

from processing.chunking.recursive_chunker import split_recursive


def split_by_sentences(text: str, max_chunk_size: int = 512) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip()
        if len(candidate) <= max_chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks or split_recursive(text, chunk_size=max_chunk_size)
