from tenacity import retry, stop_after_attempt, wait_exponential

import httpx

from config.settings import settings
from ingestion.utils.exceptions import DownloadError


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def download_url(url: str) -> tuple[bytes, str]:
    try:
        response = httpx.get(
            url,
            timeout=settings.request_timeout,
            follow_redirects=True,
            headers={"User-Agent": "HealthcareRAGBot/1.0"},
        )
        response.raise_for_status()
        content_type = response.headers.get("content-type", "application/octet-stream")
        return response.content, content_type
    except httpx.HTTPError as exc:
        raise DownloadError(f"Failed to download {url}: {exc}") from exc
