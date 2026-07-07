from generation.prompt_builder import build_prompt
from retrieval.dense import RetrievedChunk


def test_prompt_builder_includes_context_and_question():
    chunks = [
        RetrievedChunk(
            chunk_id="1",
            text="Type 2 diabetes is common in adults.",
            source="CDC",
            url="https://cdc.gov",
            title="Diabetes Basics",
            score=0.9,
        )
    ]
    system_prompt, user_prompt = build_prompt("What is type 2 diabetes?", chunks)
    assert "healthcare" in system_prompt.lower()
    assert "Type 2 diabetes" in user_prompt
    assert "What is type 2 diabetes?" in user_prompt
