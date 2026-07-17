from typing import Any

from pydantic import BaseModel


class ProcessedDocument(BaseModel):
    """Represents a cleaned document ready for chunking."""

    company: str
    ticker: str
    industry: str
    country: str

    document_type: str

    file_name: str

    pages: int

    text: str

    word_count: int

    character_count: int

    metadata: dict[str, Any]