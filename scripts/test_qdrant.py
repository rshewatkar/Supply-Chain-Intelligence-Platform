from app.embeddings.qdrant_manager import QdrantManager

manager = QdrantManager()

#manager.delete_collection()
manager.create_collection()

print()

print("Collection Exists :", manager.collection_exists())

print("Vector Count      :", manager.count_vectors())

print()

print(manager.collection_info())