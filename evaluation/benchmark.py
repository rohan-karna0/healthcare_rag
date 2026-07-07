import json
from pathlib import Path

from config.settings import settings
from evaluation.generation_eval import keyword_overlap
from evaluation.ragas_eval import run_ragas_eval
from evaluation.retrieval_eval import EVAL_QUESTIONS, precision_at_k
from generation.generator import Generator
from retrieval.retriever import Retriever


def run_benchmark() -> dict:
    retriever = Retriever()
    generator = Generator()
    retrieval_scores = []
    generation_scores = []

    for item in EVAL_QUESTIONS:
        chunks = retriever.retrieve(item["question"], top_k=5)
        retrieved_sources = [chunk.source for chunk in chunks]
        retrieval_scores.append(
            precision_at_k(retrieved_sources, item["expected_sources"], k=5)
        )

        if generator.check_health():
            result = generator.generate(item["question"], chunks)
            generation_scores.append(keyword_overlap(result.answer, item["keywords"]))

    report = {
        "retrieval_precision_at_5": sum(retrieval_scores) / max(len(retrieval_scores), 1),
        "generation_keyword_overlap": (
            sum(generation_scores) / max(len(generation_scores), 1)
            if generation_scores
            else None
        ),
        "ragas": run_ragas_eval(),
    }

    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    output_path = settings.logs_dir / "benchmark_report.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2))
