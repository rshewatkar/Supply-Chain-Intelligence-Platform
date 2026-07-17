from pydantic import BaseModel


class Chunk(BaseModel):
    """Represents one semantic chunk."""

    chunk_id: str

    company: str

    document_type: str

    chunk_index: int

    text: str

    word_count: int