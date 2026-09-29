from types import SimpleNamespace

from qdrant_client.http import models as qmodels

from retrieval.hybrid import reciprocal_rank_fusion
from retrieval.dense import DenseRetriever, RetrievedChunk


def _chunk(chunk_id: str, score: float, source: str = "CDC") -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=f"text {chunk_id}",
        source=source,
        url="https://example.com",
        title="title",
        score=score,
    )


def test_reciprocal_rank_fusion_merges_lists():
    dense = [_chunk("a", 0.9), _chunk("b", 0.8)]
    bm25 = [_chunk("b", 1.2), _chunk("c", 1.0)]
    merged = reciprocal_rank_fusion([dense, bm25], top_k=3)
    ids = [chunk.chunk_id for chunk in merged]
    assert "b" in ids
    assert len(merged) == 3


def test_dense_retriever_uses_query_points():
    class FakeEmbedder:
        def embed_text(self, text: str) -> list[float]:
            return [0.1, 0.2]

    class FakeClient:
        def __init__(self):
            self.kwargs = None

        def query_points(self, **kwargs):
            self.kwargs = kwargs
            point = qmodels.ScoredPoint(
                id="point-1",
                version=1,
                score=0.9,
                payload={"chunk_id": "chunk-1", "text": "A source text"},
            )
            return SimpleNamespace(points=[point])

    retriever = DenseRetriever.__new__(DenseRetriever)
    retriever.embedder = FakeEmbedder()
    retriever.client = FakeClient()
    retriever.collection_name = "test_collection"

    results = retriever.retrieve("test query", top_k=2)

    assert len(results) == 1
    assert results[0].text == "A source text"
    assert retriever.client.kwargs["query"] == [0.1, 0.2]
    assert retriever.client.kwargs["limit"] == 2
