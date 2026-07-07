from sentence_transformers import SentenceTransformer

from config.settings import settings
from processing.embeddings.embedding_cache import EmbeddingCache
from processing.embeddings.models import get_embedding_model_name


class Embedder:
    def __init__(self, model_name: str | None = None, use_cache: bool = True):
        self.model_name = model_name or get_embedding_model_name()
        self.model = SentenceTransformer(self.model_name)
        self.cache = EmbeddingCache() if use_cache else None

    def embed_text(self, text: str) -> list[float]:
        if self.cache:
            cached = self.cache.get(text)
            if cached is not None:
                return cached

        vector = self.model.encode(text, normalize_embeddings=True).tolist()
        if self.cache:
            self.cache.set(text, vector)
        return vector

    def embed_texts(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        vectors: list[list[float]] = []
        uncached_texts: list[str] = []
        uncached_indices: list[int] = []

        for index, text in enumerate(texts):
            if self.cache:
                cached = self.cache.get(text)
                if cached is not None:
                    vectors.append(cached)
                    continue
            vectors.append([])
            uncached_texts.append(text)
            uncached_indices.append(index)

        if uncached_texts:
            encoded = self.model.encode(
                uncached_texts,
                batch_size=batch_size,
                normalize_embeddings=True,
            )
            for idx, vector in zip(uncached_indices, encoded):
                vector_list = vector.tolist()
                vectors[idx] = vector_list
                if self.cache:
                    self.cache.set(texts[idx], vector_list)

        return vectors

    @property
    def vector_size(self) -> int:
        return len(self.embed_text("dimension probe"))
