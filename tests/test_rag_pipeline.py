from unittest.mock import MagicMock

from app.rag.rag_pipeline import RAGPipeline


def test_build_context():
    pipeline = RAGPipeline()

    documents = [
        {
            "company": "Apple",
            "file_name": "apple_report.pdf",
            "document_type": "annual_report",
            "score": 0.91,
            "text": "Apple depends on semiconductor suppliers.",
            "chunk_index": 3,
        }
    ]

    context = pipeline.build_context(
        documents
    )

    assert "Apple" in context
    assert "apple_report.pdf" in context
    assert "semiconductor suppliers" in context

    pipeline.close()


def test_empty_context():
    pipeline = RAGPipeline()

    context = pipeline.build_context([])

    assert context == ""

    pipeline.close()


def test_rag_pipeline_flow():
    pipeline = RAGPipeline()

    pipeline.retrieve_context = MagicMock(
        return_value=[
            {
                "company": "Apple",
                "file_name": "apple_report.pdf",
                "document_type": "annual_report",
                "score": 0.95,
                "text": "Apple has supplier dependencies.",
                "chunk_index": 1,
            }
        ]
    )

    pipeline.llm.generate = MagicMock(
        return_value="Apple has significant supplier dependencies."
    )

    result = pipeline.generate_answer(
        "What are Apple's supplier dependencies?"
    )

    assert result["question"] == (
        "What are Apple's supplier dependencies?"
    )

    assert (
        result["answer"]
        == "Apple has significant supplier dependencies."
    )

    assert result["source_count"] == 1

    pipeline.retrieve_context.assert_called_once()
    pipeline.llm.generate.assert_called_once()

    pipeline.close()