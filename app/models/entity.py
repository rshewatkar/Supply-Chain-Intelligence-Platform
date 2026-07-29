from pydantic import BaseModel, Field


class Entity(BaseModel):
    """
    Represents an extracted entity from a document.

    Examples
    --------
    Company:
        NVIDIA

    Product:
        H100 GPU

    Country:
        Taiwan
    """

    entity_id: str = Field(
        description="Unique identifier for the entity."
    )

    name: str = Field(
        description="Name of the extracted entity."
    )

    entity_type: str = Field(
        description="Entity category."
    )

    company: str = Field(
        description="Company associated with the source document."
    )

    ticker: str = Field(
        description="Company stock ticker."
    )

    source_document: str = Field(
        description="Document type where the entity was extracted."
    )

    file_name: str = Field(
        description="Source file name."
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score of the extracted entity."
    )

    occurrence_count: int = Field(
        default=1,
        ge=1,
        description="Number of occurrences in the document."
    )