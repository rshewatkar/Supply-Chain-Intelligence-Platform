from app.embeddings.embedding_generator import EmbeddingGenerator


def test_embedding_generator():

    generator = EmbeddingGenerator()

    embedding = generator.generate_embedding(
        "Apple designs smartphones."
    )

    assert isinstance(embedding, list)

    assert len(embedding) == 384

    assert isinstance(embedding[0], float)