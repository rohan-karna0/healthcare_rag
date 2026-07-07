import argparse
import subprocess
import sys

from generation.answer_formatter import format_answer
from generation.generator import Generator
from ingestion.ingest import IngestionPipeline
from ingestion.utils.logger import setup_logger
from processing.indexing.index_pipeline import IndexPipeline
from retrieval.retriever import Retriever

logger = setup_logger(__name__, "app.log")


def cmd_ingest(args: argparse.Namespace) -> None:
    sources = args.sources.split(",") if args.sources else None
    result = IngestionPipeline().ingest(sources=sources, index=not args.no_index)
    logger.info(
        "Ingestion complete: %s documents, %s chunks",
        result.documents_processed,
        result.chunks_created,
    )


def cmd_index(args: argparse.Namespace) -> None:
    pipeline = IndexPipeline()
    if args.reset:
        pipeline.chunk_manager.reset()
    count = pipeline.run(reset_chunks=args.reset)
    logger.info("Indexed %s chunks", count)


def cmd_query(args: argparse.Namespace) -> None:
    retriever = Retriever()
    generator = Generator(model=args.model)

    if not generator.check_health():
        logger.error("Ollama is not available at %s", generator.base_url)
        sys.exit(1)

    sources = args.sources.split(",") if args.sources else None
    chunks = retriever.retrieve(
        query=args.question,
        top_k=args.top_k,
        sources=sources,
        mode=args.mode,
    )
    result = generator.generate(args.question, chunks)
    print(format_answer(result.answer, result.sources))


def cmd_serve_ui(_: argparse.Namespace) -> None:
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"],
        check=True,
    )


def cmd_serve_api(args: argparse.Namespace) -> None:
    import uvicorn

    uvicorn.run("api.app:app", host=args.host, port=args.port, reload=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Healthcare RAG CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Crawl and ingest documents")
    ingest_parser.add_argument("--sources", help="Comma-separated source names (CDC,WHO,...)")
    ingest_parser.add_argument("--no-index", action="store_true", help="Skip indexing step")
    ingest_parser.set_defaults(func=cmd_ingest)

    index_parser = subparsers.add_parser("index", help="Index existing chunks into Qdrant")
    index_parser.add_argument("--reset", action="store_true", help="Reset chunk store before indexing")
    index_parser.set_defaults(func=cmd_index)

    query_parser = subparsers.add_parser("query", help="Ask a question")
    query_parser.add_argument("question", help="Healthcare question")
    query_parser.add_argument("--top-k", type=int, default=5)
    query_parser.add_argument("--mode", default="hybrid", choices=["hybrid", "dense", "bm25"])
    query_parser.add_argument("--sources", help="Comma-separated source filter")
    query_parser.add_argument("--model", default=None)
    query_parser.set_defaults(func=cmd_query)

    ui_parser = subparsers.add_parser("serve-ui", help="Launch Streamlit UI")
    ui_parser.set_defaults(func=cmd_serve_ui)

    api_parser = subparsers.add_parser("serve-api", help="Launch FastAPI server")
    api_parser.add_argument("--host", default="0.0.0.0")
    api_parser.add_argument("--port", type=int, default=8000)
    api_parser.set_defaults(func=cmd_serve_api)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
