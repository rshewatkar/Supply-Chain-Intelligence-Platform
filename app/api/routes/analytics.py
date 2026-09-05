from fastapi import APIRouter, HTTPException, Query

from app.analytics.risk_score_engine import RiskScoreEngine
from app.dashboard.dashboard_queries import DashboardQueries
from app.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# =========================================================
# Risk Entities
# =========================================================

@router.get("/risk/entities")
def get_risk_entities(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    """
    Return entities ordered by risk score.
    """

    engine = RiskScoreEngine()

    try:
        entities = engine.top_risky_entities(limit)

        return {
            "count": len(entities),
            "entities": entities,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve risky entities."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve risk entities.",
        ) from exc

    finally:
        engine.close()


# =========================================================
# Risk Distribution
# =========================================================

@router.get("/risk/distribution")
def get_risk_distribution():
    """
    Return distribution of entities by risk level.
    """

    queries = DashboardQueries()

    try:
        data = queries.get_risk_distribution()

        return {
            "data": data,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve risk distribution."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve risk distribution.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Dependency Metrics
# =========================================================

@router.get("/dependencies/{entity_name}")
def get_dependency_metrics(
    entity_name: str,
):
    """
    Return dependency metrics for an entity.

    Metrics include:
    - Supplier dependency
    - Country dependency
    - Tier-1 dependency
    - Tier-2 dependency
    """

    queries = DashboardQueries()

    try:
        details = queries.get_entity_details(
            entity_name
        )

        if not details:
            raise HTTPException(
                status_code=404,
                detail=f"Entity '{entity_name}' not found.",
            )

        entity = details[0]

        return {
            "entity": entity.get("name"),
            "supplier_dependency": entity.get(
                "supplier_dependency"
            ),
            "country_dependency": entity.get(
                "country_dependency"
            ),
            "tier1_dependency": entity.get(
                "tier1_dependency"
            ),
            "tier2_dependency": entity.get(
                "tier2_dependency"
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Failed to retrieve dependency metrics "
            "for %s.",
            entity_name,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dependency metrics.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Graph Analytics Summary
# =========================================================

@router.get("/graph/summary")
def get_graph_summary():
    """
    Return high-level graph analytics.
    """

    queries = DashboardQueries()

    try:
        summary = queries.get_summary()

        return summary

    except Exception as exc:
        logger.exception(
            "Failed to retrieve graph summary."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve graph summary.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Degree Centrality
# =========================================================

@router.get("/graph/degree")
def get_degree_centrality(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    """
    Return entities with highest degree centrality.
    """

    queries = DashboardQueries()

    try:
        data = queries.get_top_degree_entities(
            limit
        )

        return {
            "count": len(data),
            "entities": data,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve degree centrality."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve degree centrality.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Betweenness Centrality
# =========================================================

@router.get("/graph/betweenness")
def get_betweenness_centrality(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    """
    Return entities with highest betweenness centrality.
    """

    queries = DashboardQueries()

    try:
        data = queries.get_top_betweenness_entities(
            limit
        )

        return {
            "count": len(data),
            "entities": data,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve betweenness centrality."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve betweenness centrality.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Closeness Centrality
# =========================================================

@router.get("/graph/closeness")
def get_closeness_centrality(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    """
    Return entities with highest closeness centrality.
    """

    queries = DashboardQueries()

    try:
        data = queries.get_top_closeness_entities(
            limit
        )

        return {
            "count": len(data),
            "entities": data,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve closeness centrality."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve closeness centrality.",
        ) from exc

    finally:
        queries.close()


# =========================================================
# Community Analytics
# =========================================================

@router.get("/graph/communities")
def get_community_analytics():
    """
    Return community-level graph analytics.
    """

    queries = DashboardQueries()

    try:
        data = queries.get_community_summary()

        return {
            "count": len(data),
            "communities": data,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve community analytics."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve community analytics.",
        ) from exc

    finally:
        queries.close()