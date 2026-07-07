from urllib.parse import urlparse

from config.sources import SourceConfig


def is_allowed_url(url: str, source: SourceConfig) -> bool:
    domain = urlparse(url).netloc.lower()
    if domain not in {d.lower() for d in source.allowed_domains}:
        return False

    lowered = url.lower()
    blocked_extensions = (".jpg", ".jpeg", ".png", ".gif", ".zip", ".mp4", ".mp3")
    return not any(lowered.endswith(ext) for ext in blocked_extensions)
