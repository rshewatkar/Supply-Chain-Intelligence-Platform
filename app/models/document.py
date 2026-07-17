from typing import Any

from pydantic import BaseModel, ConfigDict


class Document(BaseModel):
    """Represents a raw document extracted from a source PDF."""

    model_config = ConfigDict(extra="allow")

    company: str
    ticker: str
    industry: str
    country: str

    document_type: str

    file_name: str
    file_path: str

    pages: int

    text: str

    metadata: dict[str, Any]