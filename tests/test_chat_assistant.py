import pytest
from unittest.mock import MagicMock
from app.chat.chat_assistant import ChatAssistant

@pytest.fixture
def chat_assistant():
    """Fixture to initialize ChatAssistant with mocked dependencies."""
    assistant = ChatAssistant()
    assistant.router = MagicMock()
    assistant.graph_queries = MagicMock()
    return assistant

def test_ask_empty_question(chat_assistant):
    """Test behavior with empty input."""
    response = chat_assistant.ask("")
    assert response["intent"] == "UNKNOWN"
    assert "Please enter a valid question" in response["answer"]

def test_ask_routing_logic(chat_assistant):
    """Test that the assistant correctly routes based on router output."""
    chat_assistant.router.route.return_value = "SUPPLIER"
    chat_assistant.graph_queries.find_entities.return_value = [{"name": "Apple"}]
    chat_assistant.graph_queries.get_supplier_relationships.return_value = [{"target": "Foxconn"}]
    
    # We mock the internal handler specifically to test routing flow
    chat_assistant._handle_supplier_question = MagicMock(return_value={"intent": "SUPPLIER", "answer": "Routed to supplier"})
    
    response = chat_assistant.ask("Who supplies Apple?")
    
    assert response["intent"] == "SUPPLIER"
    chat_assistant.router.route.assert_called_once_with("Who supplies Apple?")
    chat_assistant._handle_supplier_question.assert_called_once()

def test_handle_supplier_question_no_entities(chat_assistant):
    """Test supplier handler when no entity is found."""
    chat_assistant.graph_queries.find_entities.return_value = []
    
    response = chat_assistant._handle_supplier_question("Unknown prompt", "SUPPLIER")
    
    assert response["intent"] == "SUPPLIER"
    assert "could not identify the company" in response["answer"]

def test_close(chat_assistant):
    """Test that closing the assistant closes the graph connection."""
    chat_assistant.close()
    chat_assistant.graph_queries.close.assert_called_once()
