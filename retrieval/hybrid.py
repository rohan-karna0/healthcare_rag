from retrieval.bm25 import BM25Retriever
from retrieval.dense import DenseRetriever, RetrievedChunk


def reciprocal_rank_fusion(
    result_lists: list[list[RetrievedChunk]],
    top_k: int = 5,
    k: int = 60,
) -> list[RetrievedChunk]:
    scores: dict[str, float] = {}
    chunk_map: dict[str, RetrievedChunk] = {}

    for results in result_lists:
        for rank, chunk in enumerate(results, start=1):
            scores[chunk.chunk_id] = scores.get(chunk.chunk_id, 0.0) + 1.0 / (k + rank)
            chunk_map[chunk.chunk_id] = chunk

    ranked_ids = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)
    merged: list[RetrievedChunk] = []
    for chunk_id in ranked_ids[:top_k]:
        chunk = chunk_map[chunk_id]
        merged.append(
            RetrievedChunk(
                chunk_id=chunk.chunk_id,
                text=chunk.text,
                source=chunk.source,
                url=chunk.url,
                title=chunk.title,
                score=scores[chunk_id],
                doc_id=chunk.doc_id,
            )
        )
    return merged


class HybridRetriever:
    def __init__(self, dense: DenseRetriever | None = None, bm25: BM25Retriever | None = None):
        self.dense = dense or DenseRetriever()
        self.bm25 = bm25 or BM25Retriever()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        sources: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        dense_results = self.dense.retrieve(query, top_k=top_k * 2, sources=sources)
        bm25_results = self.bm25.retrieve(query, top_k=top_k * 2, sources=sources)
        return reciprocal_rank_fusion([dense_results, bm25_results], top_k=top_k)
