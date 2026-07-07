import hashlib
import json
from pathlib import Path

from config.settings import settings


class EmbeddingCache:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir or settings.embeddings_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "embedding_cache.json"
        self._cache = self._load()

    def _load(self) -> dict[str, list[float]]:
        if not self.cache_file.exists():
            return {}
        with self.cache_file.open(encoding="utf-8") as handle:
            return json.load(handle)

    def _save(self) -> None:
        with self.cache_file.open("w", encoding="utf-8") as handle:
            json.dump(self._cache, handle)

    @staticmethod
    def _key(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get(self, text: str) -> list[float] | None:
        return self._cache.get(self._key(text))

    def set(self, text: str, vector: list[float]) -> None:
        self._cache[self._key(text)] = vector
        self._save()
