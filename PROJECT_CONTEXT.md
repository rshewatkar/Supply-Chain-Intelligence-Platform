# Supply Chain Intelligence Platform - Project Context

## Project Overview
**Name:** Supply-Chain-Intelligence-Platform  
**Purpose:** AI-powered Supply Chain Mapping, Knowledge Graph, Risk Analytics & RAG for Electronics Manufacturing  
**Tech Stack:** Python, FastAPI, Streamlit, Neo4j, Qdrant, OpenAI/Google GenAI, LangChain

---

## Architecture Summary

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │────▶│  Neo4j KG   │────▶│  Streamlit  │
│   Backend   │     │  (Graph)    │     │  Dashboard  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Qdrant    │     │   Vector   │     │   Graph     │
│  (Vectors)  │     │   Store    │     │  Analytics  │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Directory Structure

### `/app` - Main Application Code

| Module | Purpose | Key Files |
|--------|---------|-----------|
| **analytics/** | Graph analytics & risk scoring | `risk_score_engine.py`, `community_report.py`, `tier_analysis.py`, `country_dependency.py`, `supplier_dependency.py` |
| **api/** | FastAPI REST endpoints (modular routers) | `main.py`, `routes/graph.py`, `routes/analytics.py` |
| **chat/** | Question routing for RAG & graph queries | `question_router.py`, `graph_queries.py` |
| **chunking/** | Semantic text chunking | `chunker.py`, `chunk_pipeline.py`, `chunk_utils.py` |
| **config/** | Configuration management | `settings.py` |
| **dashboard/** | Streamlit dashboard pages | `graph_dashboard.py`, `risk_dashboard_backend.py`, `dashboard_data.py`, `dashboard_queries.py` |
| **embeddings/** | Vector embeddings generation & storage | `embedding_generator.py`, `qdrant_manager.py`, `search.py`, `embeddings.py` |
| **extraction/** | Named Entity Recognition & Relationship Extraction | `entity_extractor.py`, `relationship_extractor.py`, `entity_resolver.py`, `patterns.py` |
| **graph/** | Neo4j graph database operations | `neo4j_client.py`, `graph_builder.py`, `graph_pipeline.py`, `neo4j_manager.py` |
| **ingestion/** | Document loading (PDF, etc.) | `document_loader.py`, `pdf_loader.py` |
| **models/** | Pydantic data models | `entity.py`, `relationship.py`, `chunk.py`, `document.py`, `processed_document.py` |
| **preprocessing/** | Text cleaning & processing | `document_processor.py`, `processor_pipeline.py`, `text_cleaner.py` |
| **rag/** | Retrieval-Augmented Generation pipeline | `rag_pipeline.py`, `retriever.py`, `llm.py`, `prompts.py` |
| **utils/** | Helper utilities | `logger.py`, `helpers.py`, `file_utils.py` |

### `/scripts` - Pipeline Execution Scripts

All scripts run via: `python -m scripts.<script_name>`

| Script | Function |
|--------|----------|
| `run_preprocessing.py` | Extract text from PDFs |
| `run_chunking.py` | Split text into semantic chunks |
| `run_embeddings.py` | Generate & upload vectors to Qdrant |
| `run_extraction.py` | Extract entities (NER) |
| `run_relationship_extraction.py` | Extract relationships between entities |
| `run_graph_pipeline.py` | Import entities/relationships to Neo4j |
| `run_graph_analytics.py` | Calculate centrality, communities |
| `run_risk_score_engine.py` | Calculate risk scores |
| `run_community_report.py` | Generate community reports |
| `run_tier_analysis.py` | Tier-1/Tier-2 analysis |
| `run_country_dependency.py` | Country dependency analysis |
| `run_supplier_dependency.py` | Supplier dependency analysis |
| `run_graph_dashboard.py` | Launch graph visualization dashboard |
| `run_graph_queries.py` | Run sample graph queries (suppliers, entities) |
| `run_risk_dashboard_backend.py` | Risk dashboard backend |
| `run_llm.py` | Test LLM integration |
| `run_rag.py` | Run RAG pipeline |
| `run_retriever.py` | Test retriever |
| `run_question_router.py` | Test question routing |
| `run_prompt.py` | Test prompt templates |
| `generate_metadata.py` | Generate document metadata |
| `run_rag.py` | Run RAG query pipeline |
| `run_retriever.py` | Test vector retrieval |
| `run_llm.py` | Test LLM integration |
| `run_prompt.py` | Test prompt templates |
| `run_question_router.py` | Route questions to appropriate handler |
| `generate_metadata.py` | Generate document metadata |

### `/tests` - Unit Tests

| Test File | Tests |
|-----------|-------|
| `test_chunker.py` | Chunking logic |
| `test_embeddings.py` | Embedding generation |
| `test_entity_extractor.py` | NER extraction |
| `test_risk_score_engine.py` | Risk calculations |
| `test_tier_analysis.py` | Tier analysis |
| `test_country_dependency.py` | Country dependency |
| `test_document_processor.py` | Document processing |
| `test_llm.py` | LLM integration |
| `test_logger.py` | Logging |
| `test_helpers.py` | Helper functions |


### `/data` - Data Directories
```
data/
├── raw/
│   ├── annual_reports/ (PDF)
│   ├── company_profiles/
│   ├── metadata/
│   └── wikipedia/
└── processed/ (chunks, embeddings)
```

### `/docs` - Documentation
```
docs/
└── architecture/
    └── 01_high_level_architecture.png.png
```

---

## Key Data Models

### Entity
- id, name, type (COMPANY, PRODUCT, LOCATION, PERSON, etc.)
- properties, source_document, confidence_score

### Relationship
- id, source_id, target_id, type (SUPPLIES, LOCATED_IN, PART_OF, etc.)
- properties, confidence_score

### Chunk
- id, document_id, content, metadata (page_number, section)
- embedding (list[float])

---

## Pipeline Flow

```
RAW DOCS → PREPROCESSING → CHUNKING → EMBEDDINGS → EXTRACTION
    ↓                                          ↓
DASHBOARD ← ANALYTICS ← GRAPH IMPORT ← RELATIONSHIPS
```

Run commands:
- `python -m scripts.run_preprocessing`
- `python -m scripts.run_chunking`
- `python -m scripts.run_embeddings`
- `python -m scripts.run_extraction`
- `python -m scripts.run_graph_pipeline`
- `python -m scripts.run_graph_analytics`
- `python -m scripts.run_risk_score_engine`

---

## Configuration (.env)

```
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=supply_chain

# APIs
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Paths
DATA_RAW_PATH=data/raw
DATA_PROCESSED_PATH=data/processed
```

---

## Dependencies

**Core:** fastapi, uvicorn, streamlit, pydantic  
**Data:** pandas, numpy, pymupdf, beautifulsoup4, lxml  
**AI/ML:** openai, google-genai, langchain, sentence-transformers, torch, transformers  
**Databases:** neo4j, qdrant-client, networkx

---

## API Endpoints Structure

### Router-Based Architecture (Updated Sept 5, 2026)
The API now uses a modular router-based architecture for better organization and maintainability.

**Status:** ✅ Refactored - All endpoints now properly organized into dedicated routers

### API Routers

#### 1. **Graph Router** (`app/api/routes/graph.py`)
```
GET  /graph/entities                          - List entities with limit validation
POST /graph/entities/search                   - Search entities by name/term
GET  /graph/relationships                     - Get relationships for an entity
POST /graph/suppliers                         - Get suppliers for a company
POST /graph/common-suppliers                  - Find common suppliers between two companies
```

**Features:**
- Query parameter validation with FastAPI Query (limit constraints: ge=1, le=100)
- Comprehensive error handling with try-except-finally blocks
- Structured logging using `get_logger()`
- Standardized response format with `count` field
- Request models: `EntitySearch`, `SupplierRequest`, `CommonSupplierRequest`

#### 2. **Analytics Router** (`app/api/routes/analytics.py`)
```
GET  /analytics/risk/entities                 - Top risky entities sorted by risk score
GET  /analytics/risk/distribution             - Risk distribution across entities
GET  /analytics/dependencies/{entity_name}    - Dependency metrics for entity
GET  /analytics/graph/degree                  - Entities with highest degree centrality
GET  /analytics/graph/betweenness             - Entities with highest betweenness centrality
GET  /analytics/graph/closeness               - Entities with highest closeness centrality
GET  /analytics/graph/communities             - Community-level analytics
```

**Features:**
- Risk scoring and ranking
- Multi-dimensional dependency analysis
- Graph centrality metrics (degree, betweenness, closeness)
- Community detection and analysis
- Consistent error handling and logging pattern

#### 3. **Health & Core** (`app/api/main.py`)
```
GET  /health                                  - API health check
GET  /                                        - API root info endpoint
```

### API Design Patterns (Applied Sept 5, 2026)

**Consistency Standards Applied:**
1. **Error Handling:** All endpoints use try-except-finally with HTTPException
2. **Logging:** All errors logged via `get_logger(__name__)`
3. **Parameter Validation:** Query parameters use FastAPI's Query with constraints (ge=1, le=100)
4. **Response Format:** Standardized with `count` and data fields
5. **Resource Management:** All database connections properly closed in finally blocks
6. **Code Organization:** Section comments for logical grouping

**Standard Response Format:**
```json
{
  "count": 5,
  "entities": [...]
}
```

**Standard Error Response:**
```json
{
  "detail": "Descriptive error message"
}
```

---

## Dashboard Pages (Streamlit)

1. **Graph Dashboard** (`graph_dashboard.py`)
   - Network visualization, node/relationship browsing, filter by entity type

2. **Risk Dashboard** (`risk_dashboard_backend.py`)
   - Risk score heatmap, tier analysis, country dependency charts

---

## Entity Types
- `COMPANY`, `PRODUCT`, `COUNTRY`, `INDUSTRY`, `TECHNOLOGY`

## Relationship Types (from `app/extraction/relationship_patterns.py`)
- **Company:** `PARTNERS_WITH`, `SUPPLIES_TO`, `CUSTOMER_OF`, `COMPETES_WITH`, `ACQUIRES`, `INVESTS_IN`
- **Product:** `DEVELOPS`, `MANUFACTURES`, `USES`, `SUPPORTS`
- **Geographic:** `LOCATED_IN`, `OPERATES_IN`
- **Industry:** `BELONGS_TO`, `OPERATES_INDUSTRY`
- **Technology:** `POWERED_BY`, `ENABLES`

### Supplier Query Relationship Types (`app/chat/graph_queries.py`)
The `get_suppliers()` method filters by: `SUPPLIES_TO`, `SUPPLIES`, `CUSTOMER_OF`, `PARTNERS_WITH`, `DEPENDS_ON`

## Risk Score Calculation
Based on: geographic concentration, single-source suppliers, tier-level exposure, country risk factors

---

## Testing
```bash
pytest tests/
pytest tests/test_risk_score_engine.py -v
```

---

## Docker Services
- **Neo4j** (ports: 7474, 7687)
- **Qdrant** (port: 6333)

---

## Quick Start
```bash
docker-compose up -d
pip install -r requirements.txt
uvicorn app.api.main:app --reload
streamlit run app/dashboard/graph_dashboard.py
```

---

## File Naming Conventions
- Modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case()`
- Constants: `UPPER_SNAKE_CASE`
- Tests: `test_<module_name>.py`

---

## Key Configuration Files
| File | Purpose |
|------|---------|
| `requirements.txt` | Dependencies |
| `pyproject.toml` | Project metadata |
| `.env.example` | Environment template |
| `docker-compose.yml` | Docker services |
| `pytest.ini` | Pytest config |

---

## Notes for AI Context

1. **Check** `app/config/settings.py` for configuration options
2. **Entity extraction** uses patterns in `app/extraction/patterns.py`
3. **Relationship extraction** uses patterns in `app/extraction/relationship_patterns.py`
4. **Graph queries** in `app/dashboard/dashboard_queries.py` and `app/chat/graph_queries.py`
5. **RAG prompts** in `app/rag/prompts.py`
6. **Chunking strategy** in `app/chunking/chunker.py`
7. **Embedding model** in `app/embeddings/embedding_generator.py`
8. **Supplier query** in `app/chat/graph_queries.py` filters by `SUPPLIES_TO`, `SUPPLIES`, `CUSTOMER_OF`, `PARTNERS_WITH`, `DEPENDS_ON`
9. **Virtual environment:** use `.venv` (not `venv`)
10. **API routers** organized in `app/api/routes/` with modular design (graph.py, analytics.py)
11. **Error handling pattern:** All endpoints follow try-except-finally with logging and HTTPException
12. **Parameter validation:** Use FastAPI Query() with constraints for better API documentation and validation
13. **Response standardization:** All endpoints return `{"count": N, "data": [...]}` format

---

## Project Status & Changelog

### Last Updated: September 5, 2026

#### ✅ Completed Tasks

**API Architecture Refactoring:**
- ✅ Created modular router-based API structure
  - Separated concerns into `graph.py` and `analytics.py` routers
  - Moved all endpoints from `main.py` to dedicated route files
  - Removed code duplication

**Code Quality Improvements:**
- ✅ Enhanced `graph.py` router with consistent patterns
  - Added logger integration for all endpoints
  - Implemented try-except-finally error handling
  - Added FastAPI Query parameter validation with constraints
  - Standardized response format with `count` field
  
- ✅ Refactored `main.py`
  - Removed duplicate endpoint definitions
  - Cleaned up imports (removed unused RiskScoreEngine, GraphAnalytics)
  - Centralized router registration
  - Added section comments for organization

**Error Handling & Logging:**
- ✅ All endpoints now include proper exception logging
- ✅ HTTPException with descriptive error messages
- ✅ Resource cleanup with finally blocks
- ✅ Input validation with Query constraints

**Documentation:**
- ✅ Updated PROJECT_CONTEXT.md with current API structure
- ✅ Documented design patterns and standards
- ✅ Added endpoint specifications and features

#### 📋 Active Development Areas

- **Chat/RAG Integration:** `/chat/query` endpoint (planned)
- **Document Upload:** `/documents/upload` endpoint (planned)
- **Dashboard Backend:** Streamlit integration (in progress)

#### 🔄 Architecture Components Status

| Component | Status | Notes |
|-----------|--------|-------|
| Graph Router | ✅ Complete | Refactored, tested patterns |
| Analytics Router | ✅ Complete | Full implementation |
| Health Endpoints | ✅ Complete | Basic setup done |
| Error Handling | ✅ Complete | Consistent across all routes |
| Logging | ✅ Complete | Integrated everywhere |
| Parameter Validation | ✅ Complete | Query constraints applied |
| Database Connections | ✅ Complete | Proper cleanup in finally blocks |
| Documentation | ✅ Updated | This file |


#### 🎯 Next Steps (Recommended)


1. Add unit tests for all API endpoints
2. Implement `/chat/query` endpoint with RAG pipeline
3. Implement `/documents/upload` endpoint
4. Create integration tests for full workflow
5. Performance testing and optimization
6. API rate limiting and security enhancements




