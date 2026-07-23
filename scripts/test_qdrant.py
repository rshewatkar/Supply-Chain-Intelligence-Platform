from app.embeddings.qdrant_manager import QdrantManager

manager = QdrantManager()

manager.create_collection()

print("Collection Exists:", manager.collection_exists())