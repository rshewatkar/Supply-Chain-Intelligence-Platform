from app.embeddings.embedding_generator import EmbeddingGenerator


generator = EmbeddingGenerator()

text = """
AMD develops high-performance CPUs and GPUs
for data centers, gaming, and AI workloads.
"""

embedding = generator.generate_embedding(text)

print("=" * 50)
print("Embedding Generated")
print("=" * 50)

print(f"Vector Dimension : {len(embedding)}")

print(f"First 10 Values  : {embedding[:10]}")