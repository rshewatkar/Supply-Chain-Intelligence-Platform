from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.config.settings import settings
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.utils.logger import get_logger

logger = get_logger(__name__)


class QdrantManager:
    """
    Manage all interactions with the Qdrant vector database.
    """

    def __init__(self):

        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )

        self.embedding_generator = EmbeddingGenerator()

        self.collection_name = settings.qdrant_collection

    def collection_exists(self) -> bool:
        """
        Check whether the collection exists.
        """

        collections = self.client.get_collections()

        return any(
            collection.name == self.collection_name
            for collection in collections.collections
        )

    def create_collection(self) -> None:
        """
        Create the collection if it does not exist.
        """

        if self.collection_exists():

            logger.info(
                "Collection '%s' already exists.",
                self.collection_name,
            )

            return

        dimension = (
            self.embedding_generator.get_embedding_dimension()
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=dimension,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            "Collection '%s' created successfully.",
            self.collection_name,
        )

    def recreate_collection(self) -> None:
        """
        Delete the collection (if present) and create it again.
        """

        if self.collection_exists():

            self.client.delete_collection(
                self.collection_name,
            )

            logger.info(
                "Collection '%s' deleted.",
                self.collection_name,
            )

        self.create_collection()

    def delete_collection(self) -> None:
        """
        Delete the collection.
        """

        if not self.collection_exists():

            logger.warning(
                "Collection '%s' does not exist.",
                self.collection_name,
            )

            return

        self.client.delete_collection(
            self.collection_name,
        )

        logger.info(
            "Collection '%s' deleted successfully.",
            self.collection_name,
        )