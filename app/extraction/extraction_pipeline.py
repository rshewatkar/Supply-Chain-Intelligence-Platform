from pathlib import Path

import pandas as pd

from app.extraction.entity_extractor import EntityExtractor
from app.models.entity import Entity
from app.models.processed_document import ProcessedDocument
from app.utils.file_utils import (
    load_json,
    save_json,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExtractionPipeline:
    """
    Entity extraction pipeline.

    Loads processed documents, extracts entities,
    and exports them to JSON and CSV.
    """

    def __init__(
        self,
        processed_documents_path: str = (
            "data/processed/processed_documents.json"
        ),
        output_directory: str = (
            "data/processed"
        ),
    ):

        self.processed_documents_path = (
            Path(processed_documents_path)
        )

        self.output_directory = (
            Path(output_directory)
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.extractor = EntityExtractor()

    def load_documents(
        self,
    ) -> list[ProcessedDocument]:
        """
        Load processed documents.
        """

        logger.info(
            "Loading processed documents..."
        )

        data = load_json(
            self.processed_documents_path
        )

        documents = [
            ProcessedDocument(**document)
            for document in data
        ]

        logger.info(
            f"Loaded {len(documents)} processed documents."
        )

        return documents

    def extract_entities(
        self,
        documents: list[ProcessedDocument],
    ) -> list[Entity]:
        """
        Extract entities from all documents.
        """

        logger.info(
            "Extracting entities..."
        )

        entities = []

        for document in documents:

            document_entities = (
                self.extractor.extract(document)
            )

            entities.extend(
                document_entities
            )

        logger.info(
            f"Extracted {len(entities)} entities."
        )

        return entities

    def save_entities(
        self,
        entities: list[Entity],
    ) -> None:
        """
        Save entities to JSON and CSV.
        """

        json_path = (
            self.output_directory
            / "entities.json"
        )

        csv_path = (
            self.output_directory
            / "entities.csv"
        )

        entity_dicts = [
            entity.model_dump()
            for entity in entities
        ]

        save_json(
            entity_dicts,
            json_path,
        )

        pd.DataFrame(
            entity_dicts
        ).to_csv(
            csv_path,
            index=False,
        )

        logger.info(
            f"Entities saved to {json_path}"
        )

        logger.info(
            f"Entities saved to {csv_path}"
        )

    def run(
        self,
    ) -> list[Entity]:
        """
        Execute the entity extraction pipeline.
        """

        documents = self.load_documents()

        entities = self.extract_entities(
            documents
        )

        self.save_entities(
            entities
        )

        logger.info(
            "Entity extraction completed successfully."
        )

        return entities