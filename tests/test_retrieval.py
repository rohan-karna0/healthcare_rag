from retrieval.hybrid import reciprocal_rank_fusion
from retrieval.dense import RetrievedChunk


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
