from app.extraction.entity_extractor import EntityExtractor
from app.models.processed_document import ProcessedDocument
from app.models.entity import Entity


def test_entity_extractor():

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
        NVIDIA develops H100 GPUs.

        NVIDIA partners with TSMC.

        CUDA powers AI workloads.

        NVIDIA sells products across the USA.

        H100 is widely adopted in data centers.
        """,
        word_count=26,
        character_count=170,
    )

    extractor = EntityExtractor()

    entities = extractor.extract(document)

    # -------------------------------------------------
    # Basic Assertions
    # -------------------------------------------------

    assert isinstance(entities, list)

    assert len(entities) > 0

    # -------------------------------------------------
    # Entity Object Assertions
    # -------------------------------------------------

    for entity in entities:

        assert isinstance(entity, Entity)

        assert entity.entity_id != ""

        assert entity.name != ""

        assert entity.entity_type != ""

        assert entity.company == "NVIDIA"

        assert entity.ticker == "NVDA"

        assert entity.occurrence_count >= 1

    # -------------------------------------------------
    # Ensure no duplicate entities
    # -------------------------------------------------

    names = [entity.name for entity in entities]

    assert len(names) == len(set(names))

    # -------------------------------------------------
    # Check expected entities
    # -------------------------------------------------

    extracted = {entity.name for entity in entities}

    assert "NVIDIA" in extracted

    assert "TSMC" in extracted

    assert "CUDA" in extracted

    assert "H100" in extracted

    assert "USA" in extracted