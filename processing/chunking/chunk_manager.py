import json
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from config.settings import settings
from processing.chunking.contextual_chunker import add_context_prefix
from processing.chunking.recursive_chunker import split_recursive
from processing.chunking.semantic_chunker import split_by_sentences


@dataclass
class ChunkRecord:
    chunk_id: str
    doc_id: str
    text: str
    source: str
    url: str
    title: str
    chunk_index: int


class ChunkManager:
    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or settings.chunks_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def chunk_document(
        self,
        doc_id: str,
        text: str,
        source: str,
        url: str,
        title: str,
        strategy: str = "recursive",
    ) -> list[ChunkRecord]:
        if strategy == "semantic":
            raw_chunks = split_by_sentences(text)
        else:
            raw_chunks = split_recursive(text)

        contextual_chunks = add_context_prefix(raw_chunks, title, source)
        records = [
            ChunkRecord(
                chunk_id=str(uuid.uuid4()),
                doc_id=doc_id,
                text=chunk,
                source=source,
                url=url,
                title=title,
                chunk_index=index,
            )
            for index, chunk in enumerate(contextual_chunks)
        ]
        return records

    def save_chunks(self, records: list[ChunkRecord]) -> Path:
        output_path = self.output_dir / "chunks.jsonl"
        with output_path.open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        return output_path

    def load_chunks(self) -> list[ChunkRecord]:
        output_path = self.output_dir / "chunks.jsonl"
        if not output_path.exists():
            return []

        records: list[ChunkRecord] = []
        with output_path.open(encoding="utf-8") as handle:
            for line in handle:
                data = json.loads(line)
                records.append(ChunkRecord(**data))
        return records

    def reset(self) -> None:
        output_path = self.output_dir / "chunks.jsonl"
        if output_path.exists():
            output_path.unlink()
