import pytest

from app.rag.retriever import Retriever


# =========================================================
# Validation Tests
# =========================================================

def test_retrieve_rejects_empty_query():
    retriever = Retriever.__new__(Retriever)

    with pytest.raises(ValueError):
        retriever.retrieve("")


def test_retrieve_rejects_invalid_top_k():
    retriever = Retriever.__new__(Retriever)

    with pytest.raises(ValueError):
        retriever.retrieve(
            "What is NVIDIA?",
            top_k=0,
        )


# =========================================================
# Context Tests
# =========================================================

def test_build_context():
    retriever = Retriever.__new__(Retriever)

    results = [
        {
            "score": 0.91,
            "company": "NVIDIA",
            "ticker": "NVDA",
            "document_type": "annual_report",
            "file_name": "nvidia_2025_annual_report.pdf",
            "text": "NVIDIA develops GPUs and AI computing platforms.",
            "chunk_index": 10,
        }
    ]

    context = retriever.build_context(
        results
    )

    assert "NVIDIA" in context
    assert "NVDA" in context
    assert "nvidia_2025_annual_report.pdf" in context
    assert "NVIDIA develops GPUs" in context
    assert "0.9100" in context


def test_build_context_empty_results():
    retriever = Retriever.__new__(Retriever)

    context = retriever.build_context([])

    assert context == ""


# =========================================================
# Filtering Tests
# =========================================================

def test_retrieve_relevant_filters_scores():
    retriever = Retriever.__new__(Retriever)

    retriever.search_engine = None

    # Mock retrieve directly so this test does not require Qdrant.
    retriever.retrieve = lambda query, top_k: [
        {
            "score": 0.91,
            "text": "Highly relevant chunk",
        },
        {
            "score": 0.42,
            "text": "Low relevance chunk",
        },
    ]

    results = retriever.retrieve_relevant(
        query="NVIDIA supply chain",
        top_k=5,
        min_score=0.70,
    )

    assert len(results) == 1
    assert results[0]["score"] == 0.91