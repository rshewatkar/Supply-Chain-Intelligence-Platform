from app.extraction.entity_extractor import EntityExtractor
from app.extraction.relationship_extractor import RelationshipExtractor
from app.models.processed_document import ProcessedDocument
from app.models.relationship import Relationship


def test_relationship_extraction():

    document = ProcessedDocument(
        company="NVIDIA",
        ticker="NVDA",
        industry="Semiconductor",
        country="USA",
        document_type="annual_report",
        file_name="nvidia_annual_report.pdf",
        file_path="dummy.pdf",
        pages=1,
        metadata={},
        text="""
        NVIDIA develops CUDA.

        NVIDIA partners with TSMC.

        AMD competes with Intel.

        Apple manufactures iPhone.

        NVIDIA operates in USA.
        """,
        word_count=25,
        character_count=170,
    )

    # ------------------------------------------
    # Extract entities
    # ------------------------------------------

    entity_extractor = EntityExtractor()

    entities = entity_extractor.extract(document)

    assert len(entities) > 0

    # ------------------------------------------
    # Extract relationships
    # ------------------------------------------

    relationship_extractor = RelationshipExtractor()

    print("\nExtracted Entities")
    for entity in entities:
        print(entity.entity_type, ":", entity.name)
    
    relationships = relationship_extractor.extract(
        document=document,
        entities=entities,
    )

    # ------------------------------------------
    # Basic assertions
    # ------------------------------------------

    assert isinstance(relationships, list)

    assert len(relationships) > 0

    # ------------------------------------------
    # Relationship object assertions
    # ------------------------------------------

    for relationship in relationships:

        assert isinstance(
            relationship,
            Relationship,
        )

        assert relationship.relationship_id != ""

        assert relationship.source_entity != ""

        assert relationship.target_entity != ""

        assert relationship.relationship_type != ""

        assert relationship.company == "NVIDIA"

        assert relationship.ticker == "NVDA"

        assert relationship.confidence == 1.0

        assert relationship.occurrence_count >= 1

    # ------------------------------------------
    # Ensure no duplicate relationships
    # ------------------------------------------

    keys = [
        (
            relationship.source_entity,
            relationship.relationship_type,
            relationship.target_entity,
        )
        for relationship in relationships
    ]

    assert len(keys) == len(set(keys))

    # ------------------------------------------
    # Verify expected relationship types
    # ------------------------------------------

    relationship_types = {
        relationship.relationship_type
        for relationship in relationships
    }

    assert "DEVELOPS" in relationship_types

    assert "PARTNERS_WITH" in relationship_types

    assert "COMPETES_WITH" in relationship_types

    assert "MANUFACTURES" in relationship_types

    assert "OPERATES_IN" in relationship_types

    print("\nRelationship extraction test passed.")