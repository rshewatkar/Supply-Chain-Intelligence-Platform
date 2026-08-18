from unittest.mock import MagicMock, patch

from app.dashboard.risk_dashboard_backend import (
    RiskDashboardBackend,
)


@patch(
    "app.dashboard.risk_dashboard_backend.Neo4jManager"
)
def test_get_risk_overview(mock_neo4j):

    mock_manager = MagicMock()

    mock_manager.execute_query.return_value = [
        {
            "total_entities": 10,
            "critical_entities": 1,
            "high_entities": 2,
            "medium_entities": 3,
            "low_entities": 4,
            "average_risk_score": 0.35,
            "maximum_risk_score": 0.90,
        }
    ]

    mock_neo4j.return_value = mock_manager

    backend = RiskDashboardBackend()

    result = backend.get_risk_overview()

    assert result["total_entities"] == 10
    assert result["critical_entities"] == 1
    assert result["maximum_risk_score"] == 0.90

    backend.close()


@patch(
    "app.dashboard.risk_dashboard_backend.Neo4jManager"
)
def test_get_top_risky_entities(mock_neo4j):

    mock_manager = MagicMock()

    mock_manager.execute_query.return_value = [
        {
            "entity": "NVIDIA",
            "type": "COMPANY",
            "risk_score": 0.45,
            "risk_level": "MEDIUM",
        }
    ]

    mock_neo4j.return_value = mock_manager

    backend = RiskDashboardBackend()

    result = backend.get_top_risky_entities(20)

    assert len(result) == 1
    assert result[0]["entity"] == "NVIDIA"
    assert result[0]["risk_level"] == "MEDIUM"

    backend.close()


@patch(
    "app.dashboard.risk_dashboard_backend.Neo4jManager"
)
def test_get_entity_risk(mock_neo4j):

    mock_manager = MagicMock()

    mock_manager.execute_query.return_value = [
        {
            "entity": "Apple",
            "type": "COMPANY",
            "supplier_dependency": 0.09,
            "country_dependency": 0.0,
            "tier1_dependency": 0.71,
            "tier2_dependency": 0.29,
            "risk_score": 0.31,
            "risk_level": "MEDIUM",
        }
    ]

    mock_neo4j.return_value = mock_manager

    backend = RiskDashboardBackend()

    result = backend.get_entity_risk("Apple")

    assert len(result) == 1
    assert result[0]["entity"] == "Apple"
    assert result[0]["tier1_dependency"] == 0.71

    backend.close()


@patch(
    "app.dashboard.risk_dashboard_backend.Neo4jManager"
)
def test_get_dashboard_data(mock_neo4j):

    mock_manager = MagicMock()

    mock_manager.execute_query.return_value = []

    mock_neo4j.return_value = mock_manager

    backend = RiskDashboardBackend()

    result = backend.get_dashboard_data(20)

    assert "overview" in result
    assert "top_risky_entities" in result
    assert "risk_distribution" in result
    assert "risk_by_entity_type" in result
    assert "dependency_risk" in result
    assert "centrality_risk" in result
    assert "high_risk_entities" in result

    backend.close()