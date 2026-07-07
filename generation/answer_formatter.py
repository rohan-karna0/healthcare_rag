from generation.citations import build_citations
from retrieval.dense import RetrievedChunk


def format_answer(answer: str, chunks: list[RetrievedChunk]) -> str:
    citations = build_citations(chunks)
    if not citations:
        return answer

    lines = [answer, "", "### Sources"]
    for citation in citations:
        lines.append(
            f"- [Source {citation['index']}] {citation['title']} ({citation['source']}) - {citation['url']}"
        )
    return "\n".join(lines)
