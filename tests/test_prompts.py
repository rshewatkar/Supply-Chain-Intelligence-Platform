import pytest

from app.rag.prompts import PromptBuilder


def test_build_prompt():

    builder = PromptBuilder()

    prompt = builder.build(
        question="What are NVIDIA's major products?",
        context="NVIDIA develops GPUs and AI computing platforms.",
    )

    assert "NVIDIA's major products" in prompt
    assert "NVIDIA develops GPUs" in prompt
    assert "Supply Chain Intelligence Assistant" in prompt


def test_empty_question():

    builder = PromptBuilder()

    with pytest.raises(ValueError):
        builder.build(
            question="",
            context="Some context",
        )


def test_empty_context():

    builder = PromptBuilder()

    with pytest.raises(ValueError):
        builder.build(
            question="What is NVIDIA?",
            context="",
        )


def test_system_prompt():

    builder = PromptBuilder()

    system_prompt = builder.get_system_prompt()

    assert "Supply Chain Intelligence Assistant" in system_prompt
    assert "Use ONLY the information provided in the context." in system_prompt