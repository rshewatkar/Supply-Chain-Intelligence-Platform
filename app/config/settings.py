from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.

    Values can be overridden using environment variables
    defined in the .env file.
    """

    # ==========================================
    # Project
    # ==========================================

    project_name: str = "Supply Chain Intelligence Platform"

    project_version: str = "0.1.0"

    data_dir: Path = Path("data")
    
    # ==========================================
    # Directories
    # ==========================================
  
    raw_data_dir: Path = data_dir / "raw"    

    processed_data_dir: Path = data_dir / "processed"


    # ==========================================
    # Embedding Model
    # ==========================================

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    
    # ==========================================
    # Chunking
    # ==========================================

    chunk_size: int = 1200

    chunk_overlap: int = 200

    # ==========================================
    # Qdrant
    # ==========================================

    qdrant_host: str = "localhost"

    qdrant_port: int = 6333

    qdrant_collection: str = (
        "supply_chain_documents"
    )

    # ==========================================
    # Neo4j
    # ==========================================

    neo4j_uri: str = "bolt://localhost:7687"

    neo4j_username: str = "neo4j"

    neo4j_password: str = "password"

    # ==========================================
    # FastAPI
    # ==========================================

    api_host: str = "0.0.0.0"

    api_port: int = 8000

    # ==========================================
    # Streamlit
    # ==========================================

    dashboard_port: int = 8501

    # ==========================================
    # Logging
    # ==========================================

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # =========================================
    # Random Seed
    # =========================================
    
    random_seed: int = 42


settings = Settings()