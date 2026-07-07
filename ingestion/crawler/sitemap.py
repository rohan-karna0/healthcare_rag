import httpx


def fetch_sitemap_urls(sitemap_url: str, timeout: int = 30) -> list[str]:
    try:
        response = httpx.get(sitemap_url, timeout=timeout, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError:
        return []

    urls: list[str] = []
    for line in response.text.splitlines():
        line = line.strip()
        if line.startswith("<loc>"):
            url = line.replace("<loc>", "").replace("</loc>", "").strip()
            urls.append(url)
    return urls
