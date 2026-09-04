from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.chat.graph_queries import GraphQueries

router = APIRouter(prefix="/graph", tags=["Graph"])

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

@router.get("/entities")
def get_entities(limit: int = 10):
    """
    Retrieve a list of entities.
    """
    graph_queries = GraphQueries()
    try:
        return {"entities": graph_queries.find_entities("", limit=limit)}
    finally:
        graph_queries.close()

@router.post("/entities/search")
def search_entities(search: EntitySearch):
    """
    Search for entities by name.
    """
    graph_queries = GraphQueries()
    try:
        return {"entities": graph_queries.find_entities(search.search_term, limit=search.limit)}
    finally:
        graph_queries.close()

@router.get("/relationships")
def get_relationships(entity_name: str, limit: int = 30):
    """
    Get supply chain relationships for an entity.
    """
    graph_queries = GraphQueries()
    try:
        return {"relationships": graph_queries.get_supply_chain_relationships(entity_name, limit=limit)}
    finally:
        graph_queries.close()

@router.post("/suppliers")
def get_suppliers(request: SupplierRequest):
    """
    Retrieve entities that are suppliers to a company.
    """
    graph_queries = GraphQueries()
    try:
        return {"suppliers": graph_queries.get_suppliers(request.company_name, limit=request.limit)}
    finally:
        graph_queries.close()

@router.post("/common-suppliers")
def get_common_suppliers(request: CommonSupplierRequest):
    """
    Return entities connected to both companies.
    """
    graph_queries = GraphQueries()
    try:
        return {"common_suppliers": graph_queries.get_common_suppliers(request.company_1, request.company_2, limit=request.limit)}
    finally:
        graph_queries.close()

