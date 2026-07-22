from app.embeddings.embedding_generator import EmbeddingGenerator

generator = EmbeddingGenerator()

dimension = generator.get_embedding_dimension()

text = """
AMD develops high-performance CPUs and GPUs
for AI workloads.
"""

embedding = generator.generate_embedding(text)

print("=" * 50)
print("Embedding Generator Test")
print("=" * 50)
print(f"Embedding Model     : {generator.model.__class__.__name__}")
print(f"Embedding Dimension : {dimension}")
print(f"Vector Length       : {len(embedding)}")
print(f"First 10 Values     : {embedding[:10]}")