class IngestionError(Exception):
    """Base ingestion error."""


class DownloadError(IngestionError):
    """Failed to download a resource."""


class ParseError(IngestionError):
    """Failed to parse a document."""


class CrawlError(IngestionError):
    """Crawler encountered an error."""
