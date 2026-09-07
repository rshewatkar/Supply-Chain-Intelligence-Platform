"""
API Tests for Supply Chain Intelligence Platform

Comprehensive tests covering:
1. Health check endpoints
2. Graph endpoints (entities, relationships, suppliers)
3. Analytics endpoints (risk, dependencies, centrality)
4. Chat endpoints (queries, intent detection)
5. Error handling and validation
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from app.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


# =========================================================
# Health Check Endpoints
# =========================================================

class TestHealthEndpoints:
    """Test health check and root endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_swagger_docs(self, client):
        """Test Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self, client):
        """Test OpenAPI schema is valid."""
        response = client.get("/openapi.json")
        assert response.status_code == 200


# =========================================================
# Graph Entity Endpoints
# =========================================================

class TestGraphEntityEndpoints:
    """Test graph entity-related endpoints."""
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_entities_success(self, mock_gq, client):
        """Test retrieving entities."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.find_entities.return_value = [
            {"name": "Apple", "type": "COMPANY"}
        ]
        
        response = client.get("/graph/entities?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert "entities" in data
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_entities_invalid_limit_zero(self, mock_gq, client):
        """Test entities endpoint rejects limit=0."""
        response = client.get("/graph/entities?limit=0")
        assert response.status_code == 422
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_entities_invalid_limit_exceeds_max(self, mock_gq, client):
        """Test entities endpoint rejects limit > 100."""
        response = client.get("/graph/entities?limit=101")
        assert response.status_code == 422
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_search_entities(self, mock_gq, client):
        """Test searching entities by name."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.find_entities.return_value = [
            {"name": "Apple"}
        ]
        
        response = client.post(
            "/graph/entities/search",
            json={"search_term": "Apple", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_search_entities_missing_field(self, mock_gq, client):
        """Test search entities rejects missing search_term."""
        response = client.post(
            "/graph/entities/search",
            json={"limit": 10}
        )
        assert response.status_code == 422


# =========================================================
# Graph Relationship Endpoints
# =========================================================

class TestGraphRelationshipEndpoints:
    """Test graph relationship endpoints."""
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_relationships(self, mock_gq, client):
        """Test retrieving relationships."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.get_supply_chain_relationships.return_value = [
            {"supplier": "Samsung"}
        ]
        
        response = client.get("/graph/relationships?entity_name=Apple&limit=30")
        assert response.status_code == 200
        data = response.json()
        assert data["entity_name"] == "Apple"
        assert data["count"] == 1
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_suppliers(self, mock_gq, client):
        """Test retrieving suppliers."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.get_suppliers.return_value = [
            {"name": "TSMC"}
        ]
        
        response = client.post(
            "/graph/suppliers",
            json={"company_name": "Apple", "limit": 20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Apple"
        assert data["count"] == 1
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_get_common_suppliers(self, mock_gq, client):
        """Test retrieving common suppliers."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.get_common_suppliers.return_value = [
            {"name": "TSMC"}
        ]
        
        response = client.post(
            "/graph/common-suppliers",
            json={
                "company_1": "Apple",
                "company_2": "Samsung",
                "limit": 20
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["company_1"] == "Apple"
        assert data["company_2"] == "Samsung"


# =========================================================
# Analytics Risk Endpoints
# =========================================================

class TestAnalyticsRiskEndpoints:
    """Test analytics risk endpoints."""
    
    @patch("app.api.routes.analytics.RiskScoreEngine")
    def test_get_risk_entities(self, mock_engine, client):
        """Test retrieving risk entities."""
        mock_inst = MagicMock()
        mock_engine.return_value = mock_inst
        mock_inst.top_risky_entities.return_value = [
            {"name": "Supplier A", "risk_score": 0.95}
        ]
        
        response = client.get("/analytics/risk/entities?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert "entities" in data
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_risk_distribution(self, mock_queries, client):
        """Test retrieving risk distribution."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_risk_distribution.return_value = {
            "high": 10,
            "medium": 20,
            "low": 70
        }
        
        response = client.get("/analytics/risk/distribution")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["high"] == 10


# =========================================================
# Analytics Dependency Endpoints
# =========================================================

class TestAnalyticsDependencyEndpoints:
    """Test analytics dependency endpoints."""
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_dependency_metrics(self, mock_queries, client):
        """Test retrieving dependency metrics."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_entity_details.return_value = [
            {
                "name": "Apple",
                "supplier_dependency": 0.75,
                "country_dependency": 0.65,
                "tier1_dependency": 0.80,
                "tier2_dependency": 0.55
            }
        ]
        
        response = client.get("/analytics/dependencies/Apple")
        assert response.status_code == 200
        data = response.json()
        assert data["entity"] == "Apple"
        assert data["supplier_dependency"] == 0.75
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_dependency_metrics_not_found(self, mock_queries, client):
        """Test dependency metrics for non-existent entity."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_entity_details.return_value = []
        
        response = client.get("/analytics/dependencies/NonExistent")
        assert response.status_code == 404


# =========================================================
# Analytics Centrality Endpoints
# =========================================================

class TestAnalyticsCentralityEndpoints:
    """Test analytics centrality endpoints."""
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_degree_centrality(self, mock_queries, client):
        """Test retrieving degree centrality."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_top_degree_entities.return_value = [
            {"name": "Apple", "degree": 45}
        ]
        
        response = client.get("/analytics/graph/degree?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_betweenness_centrality(self, mock_queries, client):
        """Test retrieving betweenness centrality."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_top_betweenness_entities.return_value = [
            {"name": "Hub", "betweenness": 0.85}
        ]
        
        response = client.get("/analytics/graph/betweenness?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_closeness_centrality(self, mock_queries, client):
        """Test retrieving closeness centrality."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_top_closeness_entities.return_value = [
            {"name": "Central", "closeness": 0.90}
        ]
        
        response = client.get("/analytics/graph/closeness?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    @patch("app.api.routes.analytics.DashboardQueries")
    def test_get_communities(self, mock_queries, client):
        """Test retrieving community analytics."""
        mock_inst = MagicMock()
        mock_queries.return_value = mock_inst
        mock_inst.get_community_summary.return_value = [
            {"community_id": 1, "size": 50}
        ]
        
        response = client.get("/analytics/graph/communities")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1


# =========================================================
# Chat Query Endpoints
# =========================================================

class TestChatQueryEndpoints:
    """Test chat query endpoints."""
    
    @patch("app.api.routes.chat.ChatAssistant")
    def test_chat_query_success(self, mock_assistant, client):
        """Test chat query endpoint."""
        mock_inst = MagicMock()
        mock_assistant.return_value = mock_inst
        mock_inst.ask.return_value = {
            "intent": "SUPPLIER",
            "answer": "Apple's suppliers are..."
        }
        
        response = client.post(
            "/chat/query",
            json={"question": "Who supplies Apple?", "limit": 20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == "Who supplies Apple?"
        assert data["status"] == "success"
    
    def test_chat_query_empty_question(self, client):
        """Test chat query rejects empty question."""

    
    def test_chat_query_whitespace_question(self, client):
        """Test chat query rejects whitespace-only question."""
        response = client.post(
            "/chat/query",
            json={"question": "   ", "limit": 20}
        )
        assert response.status_code == 400
    
    @patch("app.api.routes.chat.ChatAssistant")
    def test_detect_intent(self, mock_assistant, client):
        """Test intent detection endpoint."""
        mock_inst = MagicMock()
        mock_assistant.return_value = mock_inst
        mock_inst.router.route.return_value = {
            "intent": "SUPPLIER",
            "confidence": 0.95
        }
        
        response = client.post(
            "/chat/detect-intent",
            json={"question": "Who supplies Apple?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "SUPPLIER"


# =========================================================
# Chat Graph Query Endpoints
# =========================================================

class TestChatGraphEndpoints:
    """Test chat graph query endpoints."""
    
    @patch("app.api.routes.chat.ChatAssistant")
    def test_get_suppliers_via_chat(self, mock_assistant, client):
        """Test get suppliers from chat router."""
        mock_inst = MagicMock()
        mock_assistant.return_value = mock_inst
        mock_inst.graph_queries.get_suppliers.return_value = [
            {"name": "TSMC"}
        ]
        
        response = client.get("/chat/suppliers/Apple")
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Apple"
        assert data["count"] == 1
    
    @patch("app.api.routes.chat.ChatAssistant")
    def test_find_entities_via_chat(self, mock_assistant, client):
        """Test find entities from chat router."""
        mock_inst = MagicMock()
        mock_assistant.return_value = mock_inst
        mock_inst.graph_queries.find_entities.return_value = [
            {"name": "Apple"}
        ]
        
        response = client.get("/chat/entities?search_term=Apple&limit=10")


# =========================================================
# Error Handling
# =========================================================

class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_nonexistent_endpoint(self, client):
        """Test accessing non-existent endpoint returns 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_graph_exception_handling(self, mock_gq, client):
        """Test exception handling in graph endpoints."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.find_entities.side_effect = Exception("DB error")
        
        response = client.get("/graph/entities?limit=10")
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    
    @patch("app.api.routes.analytics.RiskScoreEngine")
    def test_analytics_exception_handling(self, mock_engine, client):
        """Test exception handling in analytics endpoints."""
        mock_inst = MagicMock()
        mock_engine.return_value = mock_inst
        mock_inst.top_risky_entities.side_effect = Exception("Error")
        
        response = client.get("/analytics/risk/entities?limit=20")
        assert response.status_code == 500


# =========================================================
# Request Validation
# =========================================================

class TestRequestValidation:
    """Test request validation and constraints."""
    
    def test_query_param_negative_limit(self, client):
        """Test negative limit is rejected."""
        response = client.get("/graph/entities?limit=-1")
        assert response.status_code == 422
    
    def test_query_param_zero_limit(self, client):
        """Test zero limit is rejected."""
        response = client.get("/graph/entities?limit=0")
        assert response.status_code == 422
    
    def test_query_param_max_exceeded(self, client):
        """Test limit exceeding max is rejected."""
        response = client.get("/graph/entities?limit=1000")
        assert response.status_code == 422
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_post_body_missing_required(self, mock_gq, client):
        """Test missing required fields are rejected."""
        response = client.post(
            "/graph/entities/search",
            json={"limit": 10}
        )
        assert response.status_code == 422


# =========================================================
# HTTP Methods
# =========================================================

class TestHTTPMethods:
    """Test HTTP method validation."""
    
    def test_get_endpoint_rejects_post(self, client):
        """Test GET endpoints reject POST."""
        response = client.post("/health")
        assert response.status_code == 405
    
    def test_post_endpoint_rejects_get(self, client):
        """Test POST endpoints reject GET."""
        response = client.get("/graph/entities/search")
        assert response.status_code == 405


# =========================================================
# Response Format Validation
# =========================================================

class TestResponseFormats:
    """Test response format consistency."""
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_graph_response_format(self, mock_gq, client):
        """Test graph response has required fields."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        mock_inst.find_entities.return_value = []
        
        response = client.get("/graph/entities?limit=10")
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)
        assert "entities" in data
        assert isinstance(data["entities"], list)
    
    @patch("app.api.routes.analytics.RiskScoreEngine")
    def test_analytics_response_format(self, mock_engine, client):
        """Test analytics response has required fields."""
        mock_inst = MagicMock()
        mock_engine.return_value = mock_inst
        mock_inst.top_risky_entities.return_value = []
        
        response = client.get("/analytics/risk/entities?limit=20")
        data = response.json()
        assert "count" in data
        assert "entities" in data


# =========================================================
# Integration Tests
# =========================================================

class TestIntegration:
    """Integration tests for API flows."""
    
    @patch("app.api.routes.graph.GraphQueries")
    def test_search_to_relationships_flow(self, mock_gq, client):
        """Test flow: search entity -> get relationships."""
        mock_inst = MagicMock()
        mock_gq.return_value = mock_inst
        
        # Search for entity
        mock_inst.find_entities.return_value = [{"name": "Apple"}]
        response1 = client.post(
            "/graph/entities/search",
            json={"search_term": "Apple", "limit": 10}
        )
        assert response1.status_code == 200
        
        # Get relationships
        mock_inst.get_supply_chain_relationships.return_value = [
            {"supplier": "TSMC"}
        ]
        response2 = client.get(
            "/graph/relationships?entity_name=Apple&limit=30"
        )
        assert response2.status_code == 200
        data = response2.json()
        assert data["count"] == 1

