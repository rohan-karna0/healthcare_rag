from ingestion.metadata.hashing import hash_content
from ingestion.parser.parser_factory import parse_document


def test_hash_content_is_stable():
    assert hash_content("hello") == hash_content("hello")
    assert hash_content("hello") != hash_content("world")


def test_parse_html_document():
    html = b"<html><head><title>Diabetes</title></head><body><p>Type 2 diabetes overview.</p></body></html>"
    title, text = parse_document(html, "text/html")
    assert title == "Diabetes"
    assert "Type 2 diabetes" in text


def test_parse_plain_text_document():
    content = b"Diabetes is a chronic condition affecting blood glucose."
    title, text = parse_document(content, "text/plain")
    assert title == "Text Document"
    assert "Diabetes" in text
