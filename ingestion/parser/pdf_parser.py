from io import BytesIO

from pypdf import PdfReader

from processing.cleaning.text_cleaner import clean_text


def parse_pdf(content: bytes) -> tuple[str, str]:
    reader = PdfReader(BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = clean_text("\n".join(pages))
    title = reader.metadata.title if reader.metadata and reader.metadata.title else "PDF Document"
    return title, text
