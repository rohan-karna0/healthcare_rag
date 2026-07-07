from config.settings import settings


def get_embedding_model_name() -> str:
    return settings.embedding_model


def get_vector_size(model_name: str | None = None) -> int:
    name = model_name or get_embedding_model_name()
    if "MiniLM" in name:
        return 384
    if "mpnet" in name.lower():
        return 768
    return 384
