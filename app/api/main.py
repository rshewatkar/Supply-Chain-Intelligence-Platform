from fastapi import FastAPI
from app.api.routes.graph import router as graph_router
from app.analytics.risk_score_engine import RiskScoreEngine
from app.analytics.graph_analytics import GraphAnalytics

app = FastAPI(
    title="Supply Chain Intelligence Platform API",
    description=(
        "REST API for supply chain graph analytics, "
        "risk analysis, and AI-powered supply chain queries."
    ),
    version="1.0.0",
)

# Include routers
app.include_router(graph_router)

# =========================================================
# Health Check
# =========================================================

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    """
    Check whether the API is running.
    """

    return {
        "status": "healthy",
        "service": "Supply Chain Intelligence Platform API",
    }


# =========================================================
# Root Endpoint
# =========================================================

@app.get(
    "/",
    tags=["Health"],
)
def root():
    """
    API root endpoint.
    """

    return {
        "message": (
            "Welcome to the Supply Chain Intelligence "
            "Platform API"
        ),
        "docs": "/docs",
        "health": "/health",
    }


# =========================================================
# API Endpoints
# =========================================================

@app.get("/analytics/risk-scores", tags=["Analytics"])
def get_risk_scores(limit: int = 20):
    """
    Get top risky entities.
    """
    engine = RiskScoreEngine()
    try:
        return {"risky_entities": engine.top_risky_entities(limit=limit)}
    finally:
        engine.close()


@app.get("/analytics/centrality", tags=["Analytics"])
def get_centrality_data():
    """
    Get centrality stats (a summary would be better but returning what is available).
    """
    analytics = GraphAnalytics()
    try:
        # Note: Need to implement a query for fetching centrality results in GraphAnalytics or here
        # For now, let's just return a placeholder or implement in next step if possible
        return {"message": "Centrality analytics endpoint placeholder."}
    finally:
        analytics.close()
