from app.chunking.chunker import Chunker
from app.models.processed_document import ProcessedDocument


def test_chunker():

    document = ProcessedDocument(
        company="Apple",
        ticker="AAPL",
        industry="Consumer Electronics",
        country="USA",
        document_type="annual_report",
        file_name="apple.pdf",
        pages=10,
        text="Apple " * 500,
        word_count=500,
        character_count=len("Apple " * 500),
        metadata={},
    )

    chunker = Chunker()

    chunks = chunker.split(document)

    assert len(chunks) > 0

    assert chunks[0].company == "Apple"

    assert chunks[0].ticker == "AAPL"

    assert chunks[0].chunk_index == 0