from pydantic import BaseModel, Field


class SourceChunk(BaseModel):
    chunk_id: str
    text: str
    source: str
    url: str
    title: str
    score: float


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)
    mode: str = Field(default="hybrid")
    sources: list[str] | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class HealthResponse(BaseModel):
    status: str
    ollama_available: bool
    chunks_indexed: int


class IngestRequest(BaseModel):
    sources: list[str] | None = None
    index: bool = True


class IngestResponse(BaseModel):
    documents_processed: int
    chunks_created: int
