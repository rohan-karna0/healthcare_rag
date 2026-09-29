from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_root: Path = Path(__file__).resolve().parent.parent

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "healthcare_rag"
    qdrant_local_path: str = "data/qdrant_db"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "BAAI/bge-reranker-base"

    chunk_size: int = 512
    chunk_overlap: int = 64

    top_k: int = 5
    retrieval_mode: str = "dense"
    use_reranker: bool = False

    crawl_delay_seconds: float = 1.0
    max_crawl_pages: int = 20
    request_timeout: int = 30

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def chunks_dir(self) -> Path:
        return self.data_dir / "chunks"

    @property
    def embeddings_dir(self) -> Path:
        return self.data_dir / "embeddings"

    @property
    def metadata_dir(self) -> Path:
        return self.project_root / "metadata"

    @property
    def logs_dir(self) -> Path:
        return self.project_root / "logs"

    @property
    def qdrant_path(self) -> Path:
        path = Path(self.qdrant_local_path)
        if not path.is_absolute():
            path = self.project_root / path
        return path


settings = Settings()
