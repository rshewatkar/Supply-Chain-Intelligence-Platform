from unittest.mock import MagicMock, patch

import pytest

from app.rag.llm import LLM


# =========================================================
# Initialization
# =========================================================

def test_llm_initialization():

    with patch(
        "app.rag.llm.OpenAI"
    ) as mock_client:

        llm = LLM()

        mock_client.assert_called_once()

        assert llm.get_model_name() is not None

        llm.close()


# =========================================================
# Empty Prompt
# =========================================================

def test_empty_prompt():

    with patch(
        "app.rag.llm.OpenAI"
    ):

        llm = LLM()

        with pytest.raises(ValueError):

            llm.generate("")

        llm.close()


# =========================================================
# Whitespace Prompt
# =========================================================

def test_whitespace_prompt():

    with patch(
        "app.rag.llm.OpenAI"
    ):

        llm = LLM()

        with pytest.raises(ValueError):

            llm.generate("   ")

        llm.close()


# =========================================================
# Generate Response
# =========================================================

def test_generate_response():

    with patch(
        "app.rag.llm.OpenAI"
    ) as mock_client:

        # -----------------------------------------
        # Mock OmniRoute response
        # -----------------------------------------

        mock_response = MagicMock()

        mock_response.choices = [
            MagicMock()
        ]

        mock_response.choices[0].message.content = (
            "Supplier dependency is an important "
            "supply-chain risk indicator."
        )

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .return_value
        ) = mock_response

        # -----------------------------------------
        # Initialize LLM
        # -----------------------------------------

        llm = LLM()

        # -----------------------------------------
        # Generate response
        # -----------------------------------------

        result = llm.generate(
            "Why is supplier dependency important?"
        )

        # -----------------------------------------
        # Assertions
        # -----------------------------------------

        assert isinstance(
            result,
            str,
        )

        assert (
            result
            == "Supplier dependency is an important "
            "supply-chain risk indicator."
        )

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .assert_called_once()
        )

        llm.close()


# =========================================================
# OmniRoute Empty Response
# =========================================================

def test_empty_omniroute_response():

    with patch(
        "app.rag.llm.OpenAI"
    ) as mock_client:

        # -----------------------------------------
        # Mock empty OmniRoute response
        # -----------------------------------------

        mock_response = MagicMock()

        mock_response.choices = [
            MagicMock()
        ]

        mock_response.choices[0].message.content = ""

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .return_value
        ) = mock_response

        # -----------------------------------------
        # Initialize LLM
        # -----------------------------------------

        llm = LLM()

        # -----------------------------------------
        # Empty response should raise RuntimeError
        # -----------------------------------------

        with pytest.raises(RuntimeError):

            llm.generate(
                "Test question"
            )

        llm.close()


# =========================================================
# No Choices Response
# =========================================================

def test_no_choices_response():

    with patch(
        "app.rag.llm.OpenAI"
    ) as mock_client:

        mock_response = MagicMock()

        mock_response.choices = []

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .return_value
        ) = mock_response

        llm = LLM()

        with pytest.raises(RuntimeError):

            llm.generate(
                "Test question"
            )

        llm.close()


# =========================================================
# Empty Chat Message
# =========================================================

def test_empty_chat_message():

    with patch(
        "app.rag.llm.OpenAI"
    ):

        llm = LLM()

        with pytest.raises(ValueError):

            llm.chat("")

        llm.close()


# =========================================================
# Chat Response
# =========================================================

def test_chat_response():

    with patch(
        "app.rag.llm.OpenAI"
    ) as mock_client:

        mock_response = MagicMock()

        mock_response.choices = [
            MagicMock()
        ]

        mock_response.choices[0].message.content = (
            "Supplier dependency can increase "
            "supply-chain risk."
        )

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .return_value
        ) = mock_response

        llm = LLM()

        result = llm.chat(
            "Explain supplier dependency."
        )

        assert isinstance(
            result,
            str,
        )

        assert (
            result
            == "Supplier dependency can increase "
            "supply-chain risk."
        )

        (
            mock_client
            .return_value
            .chat
            .completions
            .create
            .assert_called_once()
        )

        llm.close()