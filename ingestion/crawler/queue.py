from collections import deque

from ingestion.crawler.task import CrawlTask


class CrawlQueue:
    def __init__(self):
        self._queue: deque[CrawlTask] = deque()
        self._seen: set[str] = set()

    def add(self, task: CrawlTask) -> bool:
        if task.url in self._seen:
            return False
        self._seen.add(task.url)
        self._queue.append(task)
        return True

    def pop(self) -> CrawlTask | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def __len__(self) -> int:
        return len(self._queue)
