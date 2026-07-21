from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generate dense vector embeddings for text using
    Sentence Transformers.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):

        self.model = SentenceTransformer(model_name)

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.

        Parameters
        ----------
        text : str

        Returns
        -------
        list[float]
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Parameters
        ----------
        texts : list[str]

        Returns
        -------
        list[list[float]]
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()