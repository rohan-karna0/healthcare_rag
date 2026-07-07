from qdrant_client.http import models as qmodels

from config.settings import settings
from vectorstore.qdrant_client import get_qdrant_client


def ensure_collection(vector_size: int, collection_name: str | None = None) -> None:
    client = get_qdrant_client()
    name = collection_name or settings.qdrant_collection

    if client.collection_exists(name):
        return

    client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(
            size=vector_size,
            distance=qmodels.Distance.COSINE,
        ),
    )


def recreate_collection(vector_size: int, collection_name: str | None = None) -> None:
    client = get_qdrant_client()
    name = collection_name or settings.qdrant_collection

    if client.collection_exists(name):
        client.delete_collection(name)

    client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(
            size=vector_size,
            distance=qmodels.Distance.COSINE,
        ),
    )
