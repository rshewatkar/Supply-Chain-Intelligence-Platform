from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.chat.chat_assistant import ChatAssistant
from app.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


# =========================================================
# Request Models
# =========================================================

class ChatQuestion(BaseModel):
    """Request model for chat queries."""
    question: str
    limit: Optional[int] = 20


class IntentDetectionRequest(BaseModel):
    """Request model for intent detection."""
    question: str


# =========================================================
# Chat Query Endpoint
# =========================================================

@router.post("/query")
def chat_query(request: ChatQuestion):
    """
    Process a supply chain question and return an AI-generated answer.
    
    The assistant routes the question to the appropriate handler based on intent:
    - supplier: Questions about suppliers to a company
    - common_supplier: Questions about shared suppliers between companies
    - dependency: Questions about dependency metrics and risks
    - tier: Questions about tier-1 and tier-2 dependencies
    - general: General supply chain questions
    """
    
    assistant = ChatAssistant()
    
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )
        
        logger.info(
            "Processing chat query: %s",
            request.question,
        )
        
        response = assistant.ask(request.question)
        
        logger.info(
            "Chat query processed successfully with intent: %s",
            response.get("intent"),
        )
        
        return {
            "question": request.question,
            "response": response,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to process chat query: %s",
            request.question,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat query.",
        ) from exc
    
    finally:
        assistant.close()


# =========================================================
# Intent Detection Endpoint
# =========================================================

@router.post("/detect-intent")
def detect_intent(request: IntentDetectionRequest):
    """
    Detect the intent of a user question without processing it fully.
    
    Supported intents: supplier, common_supplier, dependency, tier, general
    """
    
    assistant = ChatAssistant()
    
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )
        
        logger.info(
            "Detecting intent for question: %s",
            request.question,
        )
        
        intent_result = assistant.router.route(request.question)
        
        logger.info(
            "Intent detected: %s with confidence: %s",
            intent_result.get("intent"),
            intent_result.get("confidence"),
        )
        
        return {
            "question": request.question,
            "intent": intent_result.get("intent"),
            "confidence": intent_result.get("confidence"),
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to detect intent for question: %s",
            request.question,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to detect intent.",
        ) from exc
    
    finally:
        assistant.close()


# =========================================================
# Supplier Query Endpoint
# =========================================================

@router.get("/suppliers/{company_name}")
def get_suppliers_for_company(
    company_name: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    """
    Get suppliers for a specific company.
    """
    
    assistant = ChatAssistant()
    
    try:
        if not company_name or not company_name.strip():
            raise HTTPException(
                status_code=400,
                detail="Company name cannot be empty.",
            )
        
        logger.info(
            "Fetching suppliers for company: %s",
            company_name,
        )
        
        suppliers = assistant.graph_queries.get_suppliers(
            company_name,
            limit=limit,
        )
        
        logger.info(
            "Found %d suppliers for %s",
            len(suppliers),
            company_name,
        )
        
        return {
            "count": len(suppliers),
            "company_name": company_name,
            "suppliers": suppliers,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to fetch suppliers for company: %s",
            company_name,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch suppliers.",
        ) from exc
    
    finally:
        assistant.close()

# =========================================================
# Common Suppliers Endpoint
# =========================================================

@router.get("/common-suppliers/{company_1}/{company_2}")
def get_common_suppliers(
    company_1: str,
    company_2: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    """
    Get suppliers shared by two companies.
    """
    
    assistant = ChatAssistant()
    
    try:
        if not company_1 or not company_1.strip():
            raise HTTPException(
                status_code=400,
                detail="Company 1 name cannot be empty.",
            )
        
        if not company_2 or not company_2.strip():
            raise HTTPException(
                status_code=400,
                detail="Company 2 name cannot be empty.",
            )
        
        logger.info(
            "Fetching common suppliers between %s and %s",
            company_1,
            company_2,
        )
        
        common_suppliers = assistant.graph_queries.get_common_suppliers(
            company_1,
            company_2,
            limit=limit,
        )
        
        logger.info(
            "Found %d common suppliers between %s and %s",
            len(common_suppliers),
            company_1,
            company_2,
        )
        
        return {
            "count": len(common_suppliers),
            "company_1": company_1,
            "company_2": company_2,
            "common_suppliers": common_suppliers,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to fetch common suppliers between %s and %s",
            company_1,
            company_2,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch common suppliers.",
        ) from exc
    
    finally:
        assistant.close()

# =========================================================
# Dependency Metrics Endpoint
# =========================================================

@router.get("/dependency-metrics/{company_name}")
def get_dependency_metrics(
    company_name: str,
):
    """
    Get dependency metrics for a company.
    """
    
    assistant = ChatAssistant()
    
    try:
        if not company_name or not company_name.strip():
            raise HTTPException(
                status_code=400,
                detail="Company name cannot be empty.",
            )
        
        logger.info(
            "Fetching dependency metrics for: %s",
            company_name,
        )
        
        metrics = assistant.graph_queries.get_dependency_metrics(
            company_name
        )
        
        logger.info(
            "Dependency metrics fetched for %s",
            company_name,
        )
        
        return {
            "company_name": company_name,
            "metrics": metrics,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to fetch dependency metrics for: %s",
            company_name,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch dependency metrics.",
        ) from exc
    
    finally:
        assistant.close()

# =========================================================
# Tier-2 Dependencies Endpoint
# =========================================================

@router.get("/tier2-dependencies/{company_name}")
def get_tier2_dependencies(
    company_name: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    """
    Get tier-2 (indirect) dependencies for a company.
    """
    
    assistant = ChatAssistant()
    
    try:
        if not company_name or not company_name.strip():
            raise HTTPException(
                status_code=400,
                detail="Company name cannot be empty.",
            )
        
        logger.info(
            "Fetching tier-2 dependencies for: %s",
            company_name,
        )
        
        tier2_deps = assistant.graph_queries.get_tier2_dependencies(
            company_name,
            limit=limit,
        )
        
        logger.info(
            "Found %d tier-2 dependencies for %s",
            len(tier2_deps),
            company_name,
        )
        
        return {
            "count": len(tier2_deps),
            "company_name": company_name,
            "tier2_dependencies": tier2_deps,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to fetch tier-2 dependencies for: %s",
            company_name,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch tier-2 dependencies.",
        ) from exc
    
    finally:
        assistant.close()

# =========================================================
# Supply Chain Relationships Endpoint
# =========================================================

@router.get("/relationships/{entity_name}")
def get_supply_chain_relationships(
    entity_name: str,
    limit: int = Query(
        default=30,
        ge=1,
        le=100,
    ),
):
    """
    Get direct supply-chain relationships for an entity.
    """
    
    assistant = ChatAssistant()
    
    try:
        if not entity_name or not entity_name.strip():
            raise HTTPException(
                status_code=400,
                detail="Entity name cannot be empty.",
            )
        
        logger.info(
            "Fetching relationships for: %s",
            entity_name,
        )
        
        relationships = assistant.graph_queries.get_supply_chain_relationships(
            entity_name,
            limit=limit,
        )
        
        logger.info(
            "Found %d relationships for %s",
            len(relationships),
            entity_name,
        )
        
        return {
            "count": len(relationships),
            "entity_name": entity_name,
            "relationships": relationships,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to fetch relationships for: %s",
            entity_name,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch relationships.",
        ) from exc
    
    finally:
        assistant.close()


# =========================================================
# Entity Search Endpoint
# =========================================================

@router.get("/entities")
def find_entities(
    search_term: str = Query(
        default="",
        description="Search term to find entities",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):
    """
    Find entities by name using search term.
    """
    
    assistant = ChatAssistant()
    
    try:
        logger.info(
            "Searching for entities with term: %s",
            search_term,
        )
        
        entities = assistant.graph_queries.find_entities(
            search_term,
            limit=limit,
        )
        
        logger.info(
            "Found %d entities matching: %s",
            len(entities),
            search_term,
        )
        
        return {
            "count": len(entities),
            "search_term": search_term,
            "entities": entities,
            "status": "success",
        }
    
    except HTTPException:
        raise
    
    except Exception as exc:
        logger.exception(
            "Failed to search entities with term: %s",
            search_term,
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to search entities.",
        ) from exc
    
    finally:
        assistant.close()
