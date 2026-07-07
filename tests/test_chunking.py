from processing.chunking.chunk_manager import ChunkManager
from processing.chunking.recursive_chunker import split_recursive


def test_recursive_chunker_respects_size():
    text = "word " * 1000
    chunks = split_recursive(text, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(len(chunk) <= 250 for chunk in chunks)


def test_chunk_manager_creates_records():
    manager = ChunkManager()
    records = manager.chunk_document(
        doc_id="doc-1",
        text="Diabetes management includes diet and exercise. " * 20,
        source="CDC",
        url="https://example.com",
        title="Diabetes Basics",
    )
    assert records
    assert records[0].source == "CDC"
    assert "CDC" in records[0].text
