from pathlib import Path
import csv

from app.extraction.entity_extractor import EntityExtractor
from app.extraction.relationship_extractor import RelationshipExtractor
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.models.processed_document import ProcessedDocument
from app.utils.file_utils import load_json, save_json
from app.utils.logger import get_logger


logger = get_logger(__name__)


class ExtractionPipeline:
    """
    End-to-end entity and relationship extraction pipeline.
    """

    def __init__(self):

        self.input_file = Path(
            "data/processed/processed_documents.json"
        )

        self.output_directory = Path(
            "data/processed"
        )

        self.entity_extractor = EntityExtractor()

        self.relationship_extractor = (
            RelationshipExtractor()
        )

    # =====================================================
    # Load Documents
    # =====================================================

    def load_documents(
        self,
    ) -> list[ProcessedDocument]:

        logger.info(
            "Loading processed documents..."
        )

        data = load_json(
            self.input_file
        )

        documents = [
            ProcessedDocument(**item)
            for item in data
        ]

        logger.info(
            f"Loaded {len(documents)} processed documents."
        )

        return documents

    # =====================================================
    # Entity Extraction
    # =====================================================

    def extract_entities(
        self,
        documents: list[ProcessedDocument],
    ) -> list[Entity]:

        logger.info(
            "Extracting entities..."
        )

        entities = []

        for document in documents:

            entities.extend(
                self.entity_extractor.extract(
                    document
                )
            )

        logger.info(
            f"Extracted {len(entities)} entities."
        )

        return entities

    # =====================================================
    # Relationship Extraction
    # =====================================================

    def extract_relationships(
        self,
        documents: list[ProcessedDocument],
        entities: list[Entity],
    ) -> list[Relationship]:
        """
        Extract relationships using the already extracted
        Entity objects to preserve entity IDs.
        """
    
        logger.info(
            "Extracting relationships..."
        )
    
        relationships = []
    
        # -------------------------------------------------
        # Group entities by document
        # -------------------------------------------------
    
        entities_by_document = {}
    
        for entity in entities:
    
            key = entity.file_name
    
            entities_by_document.setdefault(
                key,
                [],
            ).append(entity)
    
        # -------------------------------------------------
        # Extract relationships
        # -------------------------------------------------
    
        for document in documents:
    
            document_entities = entities_by_document.get(
                document.file_name,
                [],
            )
    
            relationships.extend(
                self.relationship_extractor.extract(
                    document=document,
                    entities=document_entities,
                )
            )
    
        logger.info(
            "Extracted %s relationships.",
            len(relationships),
        )
    
        return relationships                
            
    
                                                                                                        
                
    
    # =====================================================
    # Save Entities
    # =====================================================

    def save_entities(
        self,
        entities: list[Entity],
    ):

        json_path = (
            self.output_directory /
            "entities.json"
        )

        csv_path = (
            self.output_directory /
            "entities.csv"
        )

        save_json(
            [entity.model_dump() for entity in entities],
            json_path,
        )

        logger.info(
            f"Entities saved to {json_path}"
        )

        with open(
            csv_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            if not entities:
                logger.warning(
                    "No entities to save to CSV."
                )
                return
            writer = csv.DictWriter(
                file,
                fieldnames=entities[0].model_dump().keys(),
            )

            writer.writeheader()

            for entity in entities:
                writer.writerow(
                    entity.model_dump()
                )

        logger.info(
            f"Entities saved to {csv_path}"
        )

    # =====================================================
    # Save Relationships
    # =====================================================

    def save_relationships(
        self,
        relationships: list[Relationship],
    ):

        json_path = (
            self.output_directory /
            "relationships.json"
        )

        csv_path = (
            self.output_directory /
            "relationships.csv"
        )

        save_json(
            [
                relationship.model_dump()
                for relationship in relationships
            ],
            json_path,
        )

        logger.info(
            f"Relationships saved to {json_path}"
        )

        with open(
            csv_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            if not relationships:
                logger.warning(
                    "No relationships to save to CSV."
                )
                return
            writer = csv.DictWriter(
                file,
                fieldnames=relationships[0].model_dump().keys(),
            )

            writer.writeheader()

            for relationship in relationships:
                writer.writerow(
                    relationship.model_dump()
                )

        logger.info(
            f"Relationships saved to {csv_path}"
        )

    # =====================================================
    # Run Pipeline
    # =====================================================

    def run(
        self,
    ) -> tuple[
        list[Entity],
        list[Relationship],
    ]:

        documents = self.load_documents()

        entities = self.extract_entities(
            documents
        )

        relationships = (
            self.extract_relationships(
                documents,
                entities,
            )
        )

        self.save_entities(
            entities
        )

        self.save_relationships(
            relationships
        )

        logger.info(
            "Extraction pipeline completed successfully."
        )

        return (
            entities,
            relationships,
        )