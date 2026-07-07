MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024


def validate_content(content: bytes, content_type: str) -> None:
    if len(content) > MAX_DOWNLOAD_BYTES:
        raise ValueError("Content exceeds maximum allowed size")
    if not content:
        raise ValueError("Empty content")
    allowed = ("text/html", "application/pdf", "text/plain")
    if not any(content_type.startswith(kind) for kind in allowed):
        raise ValueError(f"Unsupported content type: {content_type}")
