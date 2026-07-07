from bs4 import BeautifulSoup


def parse_tables(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
            if cells:
                rows.append(" | ".join(cells))
    return "\n".join(rows)
