from dataclasses import dataclass


@dataclass
class CrawlTask:
    url: str
    source: str
    depth: int = 0
