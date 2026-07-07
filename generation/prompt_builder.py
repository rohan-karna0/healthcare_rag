from config.prompts import CONTEXT_CHUNK_TEMPLATE, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from retrieval.dense import RetrievedChunk


def build_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "No relevant context found."

    parts = []
    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            CONTEXT_CHUNK_TEMPLATE.format(
                index=index,
                source=chunk.source,
                title=chunk.title,
                url=chunk.url,
                content=chunk.text,
            )
        )
    return "\n\n".join(parts)


def build_prompt(question: str, chunks: list[RetrievedChunk]) -> tuple[str, str]:
    context = build_context(chunks)
    user_prompt = USER_PROMPT_TEMPLATE.format(context=context, question=question)
    return SYSTEM_PROMPT, user_prompt
