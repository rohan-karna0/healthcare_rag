import hashlib
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse


def normalize_url(base_url: str, link: str) -> str:
    joined = urljoin(base_url, link)
    parsed = urlparse(joined)
    return parsed._replace(fragment="").geturl()


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower()


def slugify(text: str, max_length: int = 80) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_length] or "document"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
