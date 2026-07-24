from app.embeddings.embedding_pipeline import EmbeddingPipeline

pipeline = EmbeddingPipeline(
    "data/processed/processed_documents.json"
)

chunks = pipeline.run()

print()

print("=" * 50)

print("Embedding Pipeline Completed")

print(f"Chunks Uploaded : {len(chunks)}")