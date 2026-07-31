from pathlib import Path

from app.graph.neo4j_manager import Neo4jManager
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.utils.file_utils import load_json
from app.utils.logger import get_logger


logger = get_logger(__name__)


class GraphPipeline:
    """
    Neo4j graph ingestion pipeline.

    Responsibilities
    ----------------
    1. Load extracted entities
    2. Load extracted relationships
    3. Connect to Neo4j
    4. Create constraints
    5. Import nodes
    6. Import relationships
    """

    def __init__(self):

        self.entities_path = Path(
            "data/processed/entities.json"
        )

        self.relationships_path = Path(
            "data/processed/relationships.json"
        )

        self.neo4j = Neo4jManager()

    # ======================================================
    # Load Data
    # ======================================================

    def load_entities(self) -> list[Entity]:

        logger.info("Loading entities...")

        data = load_json(self.entities_path)

        entities = [
            Entity(**item)
            for item in data
        ]

        logger.info(
            "Loaded %s entities.",
            len(entities),
        )

        return entities

    def load_relationships(
        self,
    ) -> list[Relationship]:

        logger.info("Loading relationships...")

        data = load_json(
            self.relationships_path
        )

        relationships = [
            Relationship(**item)
            for item in data
        ]

        logger.info(
            "Loaded %s relationships.",
            len(relationships),
        )

        return relationships

    # ======================================================
    # Graph Import
    # ======================================================

    def import_graph(
        self,
        clear_existing: bool = False,
    ):

        logger.info(
            "Starting Neo4j graph import..."
        )

        if not self.neo4j.verify_connection():

            raise RuntimeError(
                "Unable to connect to Neo4j."
            )

        if clear_existing:

            logger.info(
                "Clearing existing graph..."
            )

            self.neo4j.clear_graph()

        self.neo4j.create_constraints()

        entities = self.load_entities()

        relationships = (
            self.load_relationships()
        )

        logger.info(
            "Importing entity nodes..."
        )

        self.neo4j.create_entity_nodes(
            entities
        )

        logger.info(
            "Importing relationships..."
        )

        self.neo4j.create_relationships(
            relationships
        )

        logger.info(
            "Nodes           : %s",
            self.neo4j.count_nodes(),
        )

        logger.info(
            "Relationships   : %s",
            self.neo4j.count_relationships(),
        )

        self.neo4j.close()

        logger.info(
            "Graph import completed successfully."
        )