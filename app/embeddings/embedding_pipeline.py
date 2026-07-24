from __future__ import annotations

from pathlib import Path

from app.chunking.chunker import Chunker
from app.embeddings.qdrant_manager import QdrantManager
from app.models.processed_document import ProcessedDocument
from app.utils.file_utils import load_json
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingPipeline:
    """
    End-to-end embedding pipeline.

    Loads processed documents,
    creates semantic chunks,
    and uploads them into Qdrant.
    """

    def __init__(
        self,
        processed_documents_path: str | Path,
    ):

        self.processed_documents_path = Path(
            processed_documents_path
        )

        self.chunker = Chunker()

        self.qdrant = QdrantManager()

    def load_processed_documents(
        self,
    ) -> list[ProcessedDocument]:
        """
        Load processed documents from JSON.
        """

        data = load_json(
            self.processed_documents_path
        )

        documents = [
            ProcessedDocument(**item)
            for item in data
        ]

        logger.info(
            "Loaded %d processed documents.",
            len(documents),
        )

        return documents

    def create_chunks(
        self,
        documents: list[ProcessedDocument],
    ):
        """
        Generate semantic chunks from processed documents.
        """

        chunks = []

        for document in documents:

            document_chunks = self.chunker.split(document)

            chunks.extend(document_chunks)

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        return chunks

    def upload(
        self,
        chunks,
    ):
        """
        Upload chunks to Qdrant.
        """

        self.qdrant.create_collection()

        self.qdrant.upload_chunks(
            chunks
        )

        logger.info(
            "Embedding pipeline completed successfully."
        )

    def run(self):
        """
        Execute the full pipeline.
        """

        documents = self.load_processed_documents()

        chunks = self.create_chunks(
            documents
        )

        self.upload(chunks)

        return chunks