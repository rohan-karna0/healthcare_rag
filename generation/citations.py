from retrieval.dense import RetrievedChunk


def build_citations(chunks: list[RetrievedChunk]) -> list[dict]:
    citations = []
    for index, chunk in enumerate(chunks, start=1):
        citations.append(
            {
                "index": index,
                "source": chunk.source,
                "title": chunk.title,
                "url": chunk.url,
                "score": chunk.score,
            }
        )
    return citations
