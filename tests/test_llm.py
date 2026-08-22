import pytest

from app.rag.llm import LLM


def test_llm_rejects_empty_prompt():

    llm = LLM.__new__(LLM)

    llm.provider = "lm_studio"

    with pytest.raises(ValueError):
        llm.generate("")


def test_llm_rejects_whitespace_prompt():

    llm = LLM.__new__(LLM)

    llm.provider = "lm_studio"

    with pytest.raises(ValueError):
        llm.generate("   ")


def test_llm_provider():

    llm = LLM.__new__(LLM)

    llm.provider = "lm_studio"
    llm.model = "test-model"

    assert llm.get_provider() == "lm_studio"
    assert llm.get_model() == "test-model"


def test_unsupported_provider():

    llm = LLM.__new__(LLM)

    llm.provider = "unsupported"

    with pytest.raises(ValueError):
        llm.generate(
            "What is NVIDIA?"
        )


def test_lm_studio_connection_error(monkeypatch):

    from openai import APIConnectionError

    class FakeCompletions:
        def create(self, **kwargs):
            raise APIConnectionError(request=None)

    class FakeChat:
        completions = FakeCompletions()

    class FakeOpenAI:
        chat = FakeChat()

    llm = LLM.__new__(LLM)

    llm.provider = "lm_studio"
    llm.model = "test-model"
    llm.base_url = "http://localhost:1234/v1"

    monkeypatch.setattr(
        "openai.OpenAI",
        lambda **kwargs: FakeOpenAI(),
    )

    with pytest.raises(RuntimeError) as exc_info:
        llm.generate(
            "What is NVIDIA?"
        )

    assert "Could not connect to LM Studio" in str(exc_info.value)
    assert llm.base_url in str(exc_info.value)
