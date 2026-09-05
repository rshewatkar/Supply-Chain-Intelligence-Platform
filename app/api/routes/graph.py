from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.chat.graph_queries import GraphQueries
from app.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter(prefix="/graph", tags=["Graph"])


# =========================================================
# Request Models
# =========================================================

class EntitySearch(BaseModel):
    search_term: str
    limit: Optional[int] = 10


class SupplierRequest(BaseModel):
    company_name: str
    limit: Optional[int] = 20


class CommonSupplierRequest(BaseModel):
    company_1: str
    company_2: str
    limit: Optional[int] = 20


# =========================================================
# Entity Endpoints
# =========================================================

@router.get("/entities")
def get_entities(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    )
):
    """
    Retrieve a list of entities.
    """
    graph_queries = GraphQueries()

    try:
        entities = graph_queries.find_entities("", limit=limit)

        return {
            "count": len(entities),
            "entities": entities,
        }

    except Exception as exc:
        logger.exception(
            "Failed to retrieve entities."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve entities.",
        ) from exc

    finally:
        graph_queries.close()


# =========================================================
# Entity Search
# =========================================================

@router.post("/entities/search")
def search_entities(search: EntitySearch):
    """
    Search for entities by name.
    """
    graph_queries = GraphQueries()

    try:
        entities = graph_queries.find_entities(
            search.search_term,
            limit=search.limit,
        )

        return {
            "count": len(entities),
            "entities": entities,
        }

    except Exception as exc:
        logger.exception(
            f"Failed to search entities with term: {search.search_term}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to search entities.",
        ) from exc

    finally:
        graph_queries.close()


# =========================================================
# Relationships
# =========================================================

@router.get("/relationships")
def get_relationships(
    entity_name: str,
    limit: int = Query(
        default=30,
        ge=1,
        le=100,
    ),
):
    """
    Get supply chain relationships for an entity.
    """
    graph_queries = GraphQueries()

    try:
        relationships = graph_queries.get_supply_chain_relationships(
            entity_name,
            limit=limit,
        )

        return {
            "count": len(relationships),
            "entity_name": entity_name,
            "relationships": relationships,
        }

    except Exception as exc:
        logger.exception(
            f"Failed to retrieve relationships for entity: {entity_name}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve relationships.",
        ) from exc

    finally:
        graph_queries.close()


# =========================================================
# Suppliers
# =========================================================

@router.post("/suppliers")
def get_suppliers(request: SupplierRequest):
    """
    Retrieve entities that are suppliers to a company.
    """
    graph_queries = GraphQueries()

    try:
        suppliers = graph_queries.get_suppliers(
            request.company_name,
            limit=request.limit,
        )

        return {
            "count": len(suppliers),
            "company_name": request.company_name,
            "suppliers": suppliers,
        }

    except Exception as exc:
        logger.exception(
            f"Failed to retrieve suppliers for company: {request.company_name}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve suppliers.",
        ) from exc

    finally:
        graph_queries.close()


# =========================================================
# Common Suppliers
# =========================================================

@router.post("/common-suppliers")
def get_common_suppliers(request: CommonSupplierRequest):
    """
    Return entities connected to both companies.
    """
    graph_queries = GraphQueries()

    try:
        common_suppliers = graph_queries.get_common_suppliers(
            request.company_1,
            request.company_2,
            limit=request.limit,
        )

        return {
            "count": len(common_suppliers),
            "company_1": request.company_1,
            "company_2": request.company_2,
            "common_suppliers": common_suppliers,
        }

    except Exception as exc:
        logger.exception(
            f"Failed to retrieve common suppliers for companies: {request.company_1}, {request.company_2}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve common suppliers.",
        ) from exc

    finally:
        graph_queries.close()

