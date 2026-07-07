from rank_bm25 import BM25Okapi

from processing.chunking.chunk_manager import ChunkManager, ChunkRecord
from retrieval.dense import RetrievedChunk


class BM25Retriever:
    def __init__(self, chunks: list[ChunkRecord] | None = None):
        self.chunk_manager = ChunkManager()
        self.chunks = chunks or self.chunk_manager.load_chunks()
        self._tokenized = [chunk.text.lower().split() for chunk in self.chunks]
        self._bm25 = BM25Okapi(self._tokenized) if self._tokenized else None

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        sources: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        if not self._bm25 or not self.chunks:
            return []

        scores = self._bm25.get_scores(query.lower().split())
        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )

        results: list[RetrievedChunk] = []
        for index, score in ranked:
            chunk = self.chunks[index]
            if sources and chunk.source not in sources:
                continue
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    source=chunk.source,
                    url=chunk.url,
                    title=chunk.title,
                    score=float(score),
                    doc_id=chunk.doc_id,
                )
            )
            if len(results) >= top_k:
                break
        return results
