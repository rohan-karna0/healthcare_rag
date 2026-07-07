from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

from ingestion.utils.helpers import get_domain


class RobotsChecker:
    def __init__(self):
        self._parsers: dict[str, RobotFileParser] = {}

    def can_fetch(self, url: str, user_agent: str = "HealthcareRAGBot") -> bool:
        domain = get_domain(url)
        if domain not in self._parsers:
            parser = RobotFileParser()
            robots_url = urljoin(f"https://{domain}", "/robots.txt")
            parser.set_url(robots_url)
            try:
                parser.read()
            except Exception:
                return True
            self._parsers[domain] = parser
        return self._parsers[domain].can_fetch(user_agent, url)
