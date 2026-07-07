from ingestion.parser.html_parser import parse_html
from ingestion.parser.pdf_parser import parse_pdf
from ingestion.parser.table_parser import parse_tables
from ingestion.utils.exceptions import ParseError
from processing.cleaning.text_cleaner import clean_text


def parse_document(content: bytes, content_type: str) -> tuple[str, str]:
    if "pdf" in content_type:
        return parse_pdf(content)
    if content_type.startswith("text/plain"):
        text = clean_text(content.decode("utf-8", errors="ignore"))
        return "Text Document", text
    if "html" in content_type or content_type.startswith("text/"):
        title, text = parse_html(content)
        tables = parse_tables(content.decode("utf-8", errors="ignore"))
        if tables:
            text = f"{text}\n\n{tables}"
        return title, text
    raise ParseError(f"Unsupported content type: {content_type}")
