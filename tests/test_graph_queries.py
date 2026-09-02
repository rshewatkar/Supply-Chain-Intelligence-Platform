import pytest
from app.chat.graph_queries import GraphQueries
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_neo4j():
    with patch("app.chat.graph_queries.Neo4jManager") as mock:
        yield mock

def test_find_entities(mock_neo4j):
    # Setup
    instance = mock_neo4j.return_value
    instance.execute_query.return_value = [{"name": "Test Company", "entity_type": "COMPANY"}]
    
    # Execute
    queries = GraphQueries()
    results = queries.find_entities("Test")
    
    # Verify
    assert len(results) == 1
    assert results[0]["name"] == "Test Company"
    instance.execute_query.assert_called()

def test_get_suppliers(mock_neo4j):
    # Setup
    instance = mock_neo4j.return_value
    # Updated to match the new return structure from get_suppliers logic
    instance.execute_query.return_value = [{"supplier": "Supplier A", "supplier_type": "COMPANY", "relationship_types": ["CUSTOMER_OF"], "total_occurrence_count": 5}]
    
    # Execute
    queries = GraphQueries()
    results = queries.get_suppliers("Target Company")
    
    # Verify
    assert len(results) == 1
    assert results[0]["supplier"] == "Supplier A"
    assert "relationship_types" in results[0]
    instance.execute_query.assert_called()

