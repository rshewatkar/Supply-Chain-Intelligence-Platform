from unittest.mock import MagicMock, patch

from app.rag.rag_pipeline import RAGPipeline


@patch("app.rag.llm.OpenAI")
@patch("app.rag.retriever.SearchEngine")
def test_build_context(mock_search_engine, mock_openai):
    """Test building context from documents."""
    
    # Mock the SearchEngine to avoid Qdrant connection
    mock_search_engine.return_value = MagicMock()
    
    # Mock the OpenAI client to avoid API calls
    mock_openai.return_value = MagicMock()
    
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


@patch("app.rag.llm.OpenAI")
@patch("app.rag.retriever.SearchEngine")
def test_empty_context(mock_search_engine, mock_openai):
    """Test building context with empty documents."""
    
    # Mock the SearchEngine to avoid Qdrant connection
    mock_search_engine.return_value = MagicMock()
    
    # Mock the OpenAI client to avoid API calls
    mock_openai.return_value = MagicMock()
    
    pipeline = RAGPipeline()

    context = pipeline.build_context([])

    assert context == ""

    pipeline.close()


@patch("app.rag.llm.OpenAI")
@patch("app.rag.retriever.SearchEngine")
def test_rag_pipeline_flow(mock_search_engine, mock_openai):
    """Test the complete RAG pipeline flow with mocked dependencies."""
    
    # Mock the SearchEngine to avoid Qdrant connection
    mock_search_engine.return_value = MagicMock()
    
    # Mock the OpenAI client to avoid API calls
    mock_openai.return_value = MagicMock()
    
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
