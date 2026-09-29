from dataclasses import dataclass

from qdrant_client.http import models as qmodels

from config.settings import settings
from processing.embeddings.embedder import Embedder
from retrieval.metadata_filter import build_filter
from vectorstore.qdrant_client import get_qdrant_client


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    source: str
    url: str
    title: str
    score: float
    doc_id: str = ""


class DenseRetriever:
    def __init__(self, embedder: Embedder | None = None):
        self.embedder = embedder or Embedder()
        self.client = get_qdrant_client()
        self.collection_name = settings.qdrant_collection

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        sources: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        vector = self.embedder.embed_text(query)
        query_filter = build_filter(sources)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k or settings.top_k,
            query_filter=query_filter,
            with_payload=["chunk_id", "doc_id", "text", "source", "url", "title"],
        )

        return [_to_chunk(hit) for hit in response.points]


def _to_chunk(hit: qmodels.ScoredPoint) -> RetrievedChunk:
    payload = hit.payload or {}
    return RetrievedChunk(
        chunk_id=str(payload.get("chunk_id", "")),
        text=str(payload.get("text", "")),
        source=str(payload.get("source", "")),
        url=str(payload.get("url", "")),
        title=str(payload.get("title", "")),
        score=float(hit.score or 0.0),
        doc_id=str(payload.get("doc_id", "")),
    )
