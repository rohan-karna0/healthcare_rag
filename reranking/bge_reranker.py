from retrieval.dense import RetrievedChunk
from reranking.cross_encoder import CrossEncoderReranker


class BGEReranker:
    def __init__(self):
        self.encoder = CrossEncoderReranker()

    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        if not chunks:
            return []

        scores = self.encoder.score_pairs(query, [chunk.text for chunk in chunks])
        ranked = sorted(zip(chunks, scores), key=lambda item: item[1], reverse=True)

        reranked: list[RetrievedChunk] = []
        for chunk, score in ranked[:top_k]:
            reranked.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    source=chunk.source,
                    url=chunk.url,
                    title=chunk.title,
                    score=score,
                    doc_id=chunk.doc_id,
                )
            )
        return reranked
