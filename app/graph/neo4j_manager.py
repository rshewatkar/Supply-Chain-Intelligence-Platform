from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from app.config.settings import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)


class Neo4jManager:
    """
    Neo4j database manager.

    Handles:
    - Database connection
    - Connectivity verification
    - Constraint creation
    - Cypher query execution
    - Node creation
    - Relationship creation
    """

    def __init__(self):
        """
        Initialize Neo4j driver.
        """

        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
        )

    # ==========================================================
    # Connection
    # ==========================================================

    def verify_connection(self) -> bool:
        """
        Verify database connectivity.

        Returns
        -------
        bool
        """

        try:
            self.driver.verify_connectivity()

            logger.info(
                "Connected to Neo4j successfully."
            )

            return True

        except Exception as error:

            logger.error(error)

            return False

    def close(self):
        """
        Close Neo4j connection.
        """

        self.driver.close()

        logger.info("Neo4j connection closed.")

    # ==========================================================
    # Cypher Execution
    # ==========================================================

    def execute_query(
        self,
        query: str,
        parameters: dict | None = None,
    ):
        """
        Execute a Cypher query.

        Parameters
        ----------
        query : str

        parameters : dict

        Returns
        -------
        list
        """

        try:

            with self.driver.session() as session:

                result = session.run(
                    query,
                    parameters or {},
                )

                return list(result)

        except Neo4jError as error:

            logger.error(error)

            raise

    # ==========================================================
    # Constraints
    # ==========================================================

    def create_constraints(self):
        """
        Create uniqueness constraints.
        """

        queries = [

            """
            CREATE CONSTRAINT entity_id_unique
            IF NOT EXISTS

            FOR (e:Entity)

            REQUIRE e.entity_id IS UNIQUE
            """,

            """
            CREATE CONSTRAINT relationship_id_unique
            IF NOT EXISTS

            FOR ()-[r:RELATED_TO]-()

            REQUIRE r.relationship_id IS UNIQUE
            """,

        ]

        for query in queries:

            self.execute_query(query)

        logger.info(
            "Neo4j constraints created."
        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def count_nodes(self) -> int:
        """
        Return total nodes.
        """

        query = """
        MATCH (n)

        RETURN count(n) AS total
        """

        result = self.execute_query(query)

        return result[0]["total"]

    def count_relationships(self) -> int:
        """
        Return total relationships.
        """

        query = """
        MATCH ()-[r]->()

        RETURN count(r) AS total
        """

        result = self.execute_query(query)

        return result[0]["total"]

    # ==========================================================
    # Graph Maintenance
    # ==========================================================

    def clear_graph(self):
        """
        Delete entire graph.
        """

        self.execute_query(
            """
            MATCH (n)

            DETACH DELETE n
            """
        )

        logger.info(
            "Graph cleared successfully."
        )
        
    def create_entity_nodes(
        self,
        entities,
    ):    
        """
        Create Entity nodes in Neo4j.
        """
    
        query = """
        MERGE (e:Entity {
            entity_id: $entity_id
        })
    
        SET
            e.name = $name,
            e.entity_type = $entity_type,
            e.company = $company,
            e.ticker = $ticker,
            e.source_document = $source_document,
            e.file_name = $file_name,
            e.confidence = $confidence,
            e.occurrence_count = $occurrence_count
        """
    
        with self.driver.session() as session:
    
            for entity in entities:
    
                session.run(
                    query,
                    entity.model_dump(),
                )
    
        logger.info(
            "Imported %s entity nodes.",
            len(entities),
        )
    
    def create_relationships(
        self,
        relationships,
    ):
        """
        Create relationships between Entity nodes.
        """
    
        query = """
        MATCH (source:Entity {
            entity_id: $source_entity_id
        })
    
        MATCH (target:Entity {
            entity_id: $target_entity_id
        })
    
        MERGE (source)-[r:RELATED_TO {
            relationship_id: $relationship_id
        }]->(target)
    
        SET
            r.relationship_type = $relationship_type,
            r.company = $company,
            r.ticker = $ticker,
            r.source_document = $source_document,
            r.file_name = $file_name,
            r.confidence = $confidence,
            r.occurrence_count = $occurrence_count
        """
    
        with self.driver.session() as session:
    
            for relationship in relationships:
    
                session.run(
                    query,
                    relationship.model_dump(),
                )
    
        logger.info(
            "Imported %s relationships.",
            len(relationships),
        )
    
    