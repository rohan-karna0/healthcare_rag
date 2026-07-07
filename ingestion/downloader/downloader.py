from pathlib import Path

from config.settings import settings
from ingestion.downloader.retry import download_url
from ingestion.downloader.validator import validate_content
from ingestion.utils.helpers import ensure_dir, file_hash, slugify
from ingestion.utils.logger import setup_logger

logger = setup_logger(__name__, "downloader.log")


class Downloader:
    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or settings.raw_dir
        ensure_dir(self.output_dir)

    def save(self, url: str, source: str, content: bytes, content_type: str) -> Path:
        validate_content(content, content_type)
        source_dir = ensure_dir(self.output_dir / source)
        extension = ".pdf" if "pdf" in content_type else ".html"
        filename = f"{slugify(url)}{extension}"
        path = source_dir / filename
        path.write_bytes(content)
        logger.info("Saved %s", path)
        return path

    def download(self, url: str, source: str) -> tuple[Path, bytes, str]:
        content, content_type = download_url(url)
        path = self.save(url, source, content, content_type)
        return path, content, content_type
