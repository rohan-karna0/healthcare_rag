from dataclasses import dataclass

import httpx

from config.settings import settings
from generation.prompt_builder import build_prompt
from retrieval.dense import RetrievedChunk


@dataclass
class GenerationResult:
    answer: str
    sources: list[RetrievedChunk]


class Generator:
    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or settings.ollama_model
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")

    def check_health(self) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def generate(self, question: str, chunks: list[RetrievedChunk]) -> GenerationResult:
        system_prompt, user_prompt = build_prompt(question, chunks)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }

        response = httpx.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "")
        return GenerationResult(answer=answer, sources=chunks)

    def generate_stream(self, question: str, chunks: list[RetrievedChunk]):
        system_prompt, user_prompt = build_prompt(question, chunks)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": True,
        }

        with httpx.stream(
            "POST",
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120.0,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                import json

                data = json.loads(line)
                content = data.get("message", {}).get("content", "")
                if content:
                    yield content
