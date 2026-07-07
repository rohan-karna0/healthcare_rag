from qdrant_client import QdrantClient

from config.settings import settings
from ingestion.utils.logger import setup_logger

logger = setup_logger(__name__, "qdrant.log")

_client: QdrantClient | None = None


def _local_client() -> QdrantClient:
    settings.qdrant_path.mkdir(parents=True, exist_ok=True)
    logger.info("Using local Qdrant storage at %s", settings.qdrant_path)
    return QdrantClient(path=str(settings.qdrant_path))


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is not None:
        return _client

    if settings.qdrant_url:
        try:
            kwargs = {"url": settings.qdrant_url}
            if settings.qdrant_api_key:
                kwargs["api_key"] = settings.qdrant_api_key
            client = QdrantClient(**kwargs)
            client.get_collections()
            logger.info("Connected to Qdrant server at %s", settings.qdrant_url)
            _client = client
            return _client
        except Exception as exc:
            logger.warning("Qdrant server unavailable (%s). Using local path storage.", exc)

    _client = _local_client()
    return _client
