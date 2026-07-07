import time
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config.settings import settings
from config.sources import SourceConfig, get_sources
from ingestion.crawler.filters import is_allowed_url
from ingestion.crawler.queue import CrawlQueue
from ingestion.crawler.robots import RobotsChecker
from ingestion.crawler.task import CrawlTask
from ingestion.utils.helpers import normalize_url
from ingestion.utils.logger import setup_logger

logger = setup_logger(__name__, "crawler.log")


class Crawler:
    def __init__(self, max_pages: int | None = None, delay: float | None = None):
        self.max_pages = max_pages or settings.max_crawl_pages
        self.delay = delay or settings.crawl_delay_seconds
        self.robots = RobotsChecker()
        self.client = httpx.Client(
            timeout=settings.request_timeout,
            follow_redirects=True,
            headers={"User-Agent": "HealthcareRAGBot/1.0"},
        )

    def crawl(self, sources: list[str] | None = None) -> list[dict]:
        queue = CrawlQueue()
        discovered: list[dict] = []

        for source in get_sources(sources):
            for seed in source.seed_urls:
                queue.add(CrawlTask(url=seed, source=source.name, depth=0))

        while queue and len(discovered) < self.max_pages:
            task = queue.pop()
            if task is None:
                break

            source_config = next(s for s in get_sources([task.source]) if s.name == task.source)
            if not is_allowed_url(task.url, source_config):
                continue
            if not self.robots.can_fetch(task.url):
                continue

            try:
                response = self.client.get(task.url)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                logger.warning("Failed to crawl %s: %s", task.url, exc)
                continue

            content_type = response.headers.get("content-type", "")
            discovered.append(
                {
                    "url": task.url,
                    "source": task.source,
                    "content": response.content,
                    "content_type": content_type,
                    "title": _extract_title(response.text),
                }
            )
            logger.info("Crawled %s", task.url)

            if "text/html" in content_type and task.depth < 1:
                for link in _extract_links(response.text, task.url):
                    if is_allowed_url(link, source_config):
                        queue.add(CrawlTask(url=link, source=task.source, depth=task.depth + 1))

            time.sleep(self.delay)

        return discovered


def _extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Untitled"


def _extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for anchor in soup.find_all("a", href=True):
        links.append(normalize_url(base_url, anchor["href"]))
    return links
