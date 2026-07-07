from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import uuid

from config.settings import settings
from ingestion.crawler.crawler import Crawler
from ingestion.downloader.downloader import Downloader
from ingestion.metadata.hashing import hash_content
from ingestion.metadata.repository import DocumentRecord, MetadataRepository
from ingestion.parser.parser_factory import parse_document
from ingestion.utils.helpers import ensure_dir, slugify
from ingestion.utils.logger import setup_logger
from processing.chunking.chunk_manager import ChunkManager
from processing.cleaning.text_cleaner import clean_text
from processing.indexing.index_pipeline import IndexPipeline

logger = setup_logger(__name__, "ingest.log")


@dataclass
class IngestionResult:
    documents_processed: int
    chunks_created: int


class IngestionPipeline:
    def __init__(self):
        self.crawler = Crawler()
        self.downloader = Downloader()
        self.metadata = MetadataRepository()
        self.chunk_manager = ChunkManager()
        self.index_pipeline = IndexPipeline()
        ensure_dir(settings.processed_dir)

    def ingest(self, sources: list[str] | None = None, index: bool = True) -> IngestionResult:
        pages = self.crawler.crawl(sources)
        if not pages:
            pages = self._load_sample_documents()

        documents_processed = 0
        all_chunks = []

        for page in pages:
            url = page["url"]
            source = page["source"]
            content = page["content"]
            content_type = page.get("content_type", "text/html")

            self.metadata.log_crawl({"url": url, "source": source, "status": "success"})

            try:
                title, text = parse_document(content, content_type)
            except Exception as exc:
                logger.warning("Parse failed for %s: %s", url, exc)
                continue

            text = clean_text(text)
            if len(text) < 100:
                continue

            doc_id = str(uuid.uuid4())
            content_hash = hash_content(text)
            processed_path = settings.processed_dir / source / f"{slugify(title)}.txt"
            ensure_dir(processed_path.parent)
            processed_path.write_text(text, encoding="utf-8")

            self.metadata.save_document(
                DocumentRecord(
                    doc_id=doc_id,
                    source=source,
                    url=url,
                    title=title,
                    content_hash=content_hash,
                    processed_path=str(processed_path),
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
            )
            self.metadata.log_download({"url": url, "source": source, "path": str(processed_path)})

            chunks = self.chunk_manager.chunk_document(
                doc_id=doc_id,
                text=text,
                source=source,
                url=url,
                title=title,
            )
            all_chunks.extend(chunks)
            documents_processed += 1

        if all_chunks:
            self.chunk_manager.save_chunks(all_chunks)

        chunks_created = len(all_chunks)
        if index and all_chunks:
            self.index_pipeline.uploader.upload_chunks(
                all_chunks,
                self.index_pipeline.embedder,
            )

        return IngestionResult(
            documents_processed=documents_processed,
            chunks_created=chunks_created,
        )

    def _load_sample_documents(self) -> list[dict]:
        logger.info("No crawl results. Loading bundled sample healthcare documents.")
        sample_dir = settings.project_root / "data" / "samples"
        pages = []
        if not sample_dir.exists():
            return pages

        for path in sample_dir.glob("*.txt"):
            content = path.read_text(encoding="utf-8").encode("utf-8")
            source = path.stem.split("_")[0].upper()
            pages.append(
                {
                    "url": f"https://example.local/{path.name}",
                    "source": source,
                    "content": content,
                    "content_type": "text/plain",
                    "title": path.stem.replace("_", " ").title(),
                }
            )
        return pages
