from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sqlite3

from config.settings import settings


@dataclass(frozen=True)
class DocumentRecord:
    doc_id: str
    source: str
    url: str
    title: str
    content_hash: str
    processed_path: str
    created_at: str


class MetadataRepository:
    def __init__(self, database_path: str | Path | None = None):
        self.database_path = Path(database_path) if database_path else settings.metadata_dir / "ingestion.db"
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS documents (
                    doc_id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    processed_path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS ingestion_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def save_document(self, record: DocumentRecord) -> None:
        with self._connect() as connection:
            connection.execute(
                """INSERT OR REPLACE INTO documents
                (doc_id, source, url, title, content_hash, processed_path, created_at)
                VALUES (:doc_id, :source, :url, :title, :content_hash,
                        :processed_path, :created_at)""",
                asdict(record),
            )

    def log_crawl(self, event: dict) -> None:
        self._log_event("crawl", event)

    def log_download(self, event: dict) -> None:
        self._log_event("download", event)

    def _log_event(self, event_type: str, payload: dict) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO ingestion_events (event_type, payload) VALUES (?, ?)",
                (event_type, json.dumps(payload, sort_keys=True)),
            )