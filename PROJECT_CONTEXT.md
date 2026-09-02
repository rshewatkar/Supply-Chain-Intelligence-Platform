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
| **api/** | FastAPI REST endpoints | `main.py` |
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

## API Endpoints (app/api/main.py)

```
GET  /health
POST /documents/upload
GET  /documents/{id}
GET  /entities
POST /entities/search
GET  /relationships
GET  /analytics/risk-scores
GET  /analytics/centrality
POST /chat/query
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