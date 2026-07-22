from sentence_transformers import SentenceTransformer

from app.config.settings import settings


class EmbeddingGenerator:
    """
    Generate dense vector embeddings using a Sentence Transformer model.
    """

    def __init__(self):
        """Load the embedding model defined in the application settings."""

        self.model = SentenceTransformer(settings.embedding_model)

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        list[float]
            Embedding vector.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Parameters
        ----------
        texts : list[str]
            List of input texts.

        Returns
        -------
        list[list[float]]
            List of embedding vectors.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def get_embedding_dimension(self) -> int:
        """
        Return the embedding dimension of the loaded model.

        Returns
        -------
        int
            Dimension of the embedding vectors.
        """

        return self.model.get_sentence_embedding_dimension()