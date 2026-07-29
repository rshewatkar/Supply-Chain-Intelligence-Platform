from pydantic import BaseModel


class Relationship(BaseModel):
    """
    Represents a relationship between two entities.
    """

    relationship_id: str

    source_entity: str

    source_entity_type: str

    target_entity: str

    target_entity_type: str

    relationship_type: str

    company: str

    ticker: str

    source_document: str

    file_name: str

    confidence: float = 1.0

    occurrence_count: int = 1