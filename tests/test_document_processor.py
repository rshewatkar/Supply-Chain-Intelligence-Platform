from app.models.document import Document
from app.preprocessing.document_processor import DocumentProcessor


def test_document_processor():

    document = Document(
        company="Apple",
        ticker="AAPL",
        industry="Consumer Electronics",
        country="USA",
        document_type="annual_report",
        file_name="apple.pdf",
        file_path="data/apple.pdf",
        pages=10,
        text="Apple     manufactures      iPhone.\n\n\n",
        metadata={},
    )

    processed = DocumentProcessor.process(document)

    assert processed.company == "Apple"

    assert processed.word_count > 0

    assert processed.character_count > 0

    assert "manufactures iPhone" in processed.text