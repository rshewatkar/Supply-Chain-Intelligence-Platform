from pydantic import BaseModel


class Chunk(BaseModel):
    """Represents one semantic chunk."""

    chunk_id: str

    company: str

    ticker: str

    document_type: str

    file_name: str

    chunk_index: int

    text: str

    word_count: int

    character_count: int

    page_count: int