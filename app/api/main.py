from fastapi import FastAPI
from app.api.routes.graph import router as graph_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title="Supply Chain Intelligence Platform API",
    description=(
        "REST API for supply chain graph analytics, "
        "risk analysis, and AI-powered supply chain queries."
    ),
    version="1.0.0",
)

# =========================================================
# Include Routers
# =========================================================

app.include_router(graph_router)
app.include_router(analytics_router)
app.include_router(chat_router)


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

