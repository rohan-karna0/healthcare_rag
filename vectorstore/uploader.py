import uuid

from qdrant_client.http import models as qmodels

from config.settings import settings
from ingestion.utils.logger import setup_logger
from processing.chunking.chunk_manager import ChunkRecord
from processing.embeddings.embedder import Embedder
from vectorstore.collections import ensure_collection
from vectorstore.qdrant_client import get_qdrant_client

logger = setup_logger(__name__, "uploader.log")


class VectorUploader:
    def __init__(self, vector_size: int):
        self.vector_size = vector_size
        self.client = get_qdrant_client()
        self.collection_name = settings.qdrant_collection

    def upload_chunks(self, chunks: list[ChunkRecord], embedder: Embedder, batch_size: int = 64) -> None:
        ensure_collection(self.vector_size, self.collection_name)
        texts = [chunk.text for chunk in chunks]

        for start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[start : start + batch_size]
            batch_texts = texts[start : start + batch_size]
            vectors = embedder.embed_texts(batch_texts)

            points = [
                qmodels.PointStruct(
                    id=str(uuid.uuid5(uuid.NAMESPACE_URL, chunk.chunk_id)),
                    vector=vector,
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "doc_id": chunk.doc_id,
                        "text": chunk.text,
                        "source": chunk.source,
                        "url": chunk.url,
                        "title": chunk.title,
                        "chunk_index": chunk.chunk_index,
                    },
                )
                for chunk, vector in zip(batch_chunks, vectors)
            ]

            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info("Uploaded batch %s-%s", start + 1, start + len(batch_chunks))
