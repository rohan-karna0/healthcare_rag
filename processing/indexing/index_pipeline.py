from ingestion.utils.logger import setup_logger
from processing.chunking.chunk_manager import ChunkManager, ChunkRecord
from processing.embeddings.embedder import Embedder
from vectorstore.uploader import VectorUploader

logger = setup_logger(__name__, "indexing.log")


class IndexPipeline:
    def __init__(self):
        self.chunk_manager = ChunkManager()
        self.embedder = Embedder()
        self.uploader = VectorUploader(self.embedder.vector_size)

    def run(self, reset_chunks: bool = False) -> int:
        if reset_chunks:
            self.chunk_manager.reset()

        chunks = self.chunk_manager.load_chunks()
        if not chunks:
            logger.warning("No chunks found. Run ingestion and chunking first.")
            return 0

        logger.info("Indexing %s chunks into Qdrant", len(chunks))
        self.uploader.upload_chunks(chunks, self.embedder)
        return len(chunks)

    def index_records(self, records: list[ChunkRecord]) -> int:
        if not records:
            return 0
        self.chunk_manager.save_chunks(records)
        self.uploader.upload_chunks(records, self.embedder)
        return len(records)
