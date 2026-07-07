from fastapi import APIRouter, HTTPException

from api.schemas import (
    HealthResponse,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    SourceChunk,
)
from generation.answer_formatter import format_answer
from generation.generator import Generator
from ingestion.ingest import IngestionPipeline
from processing.chunking.chunk_manager import ChunkManager
from retrieval.retriever import Retriever

router = APIRouter()
retriever = Retriever()
generator = Generator()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    chunks = ChunkManager().load_chunks()
    return HealthResponse(
        status="ok",
        ollama_available=generator.check_health(),
        chunks_indexed=len(chunks),
    )


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    if not generator.check_health():
        raise HTTPException(
            status_code=503,
            detail="Ollama is not available. Install Ollama and pull a model.",
        )

    chunks = retriever.retrieve(
        query=request.question,
        top_k=request.top_k,
        sources=request.sources,
        mode=request.mode,
    )
    result = generator.generate(request.question, chunks)
    answer = format_answer(result.answer, result.sources)

    return QueryResponse(
        answer=answer,
        sources=[
            SourceChunk(
                chunk_id=chunk.chunk_id,
                text=chunk.text,
                source=chunk.source,
                url=chunk.url,
                title=chunk.title,
                score=chunk.score,
            )
            for chunk in result.sources
        ],
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    pipeline = IngestionPipeline()
    result = pipeline.ingest(sources=request.sources, index=request.index)
    return IngestResponse(
        documents_processed=result.documents_processed,
        chunks_created=result.chunks_created,
    )
