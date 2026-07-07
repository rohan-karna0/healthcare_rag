from bs4 import BeautifulSoup

from processing.cleaning.html_cleaner import strip_html


def parse_html(content: bytes) -> tuple[str, str]:
    html = content.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
    text = strip_html(html)
    return title, text
