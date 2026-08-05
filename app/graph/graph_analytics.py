from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class GraphAnalytics:
    """
    Graph analytics using the Neo4j Graph Data Science library.

    Provides:
    - Graph Projection
    - Degree Centrality
    - Betweenness Centrality
    """

    GRAPH_NAME = "supply_chain_graph"

    def __init__(self):

        self.neo4j = Neo4jManager()

    # =====================================================
    # Graph Projection
    # =====================================================

    def create_projection(self):
        """
        Create an in-memory graph projection.
        """

        logger.info("Creating GDS graph projection...")

        # Drop previous projection if it exists
        self.neo4j.execute_query(
            """
            CALL gds.graph.drop(
                $graph_name,
                false
            )
            """,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )

        query = """
        CALL gds.graph.project(

            $graph_name,

            'Entity',
            '*'

                                                               
        )
        """

        self.neo4j.execute_query(
            query,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )

        logger.info("Projection created successfully.")

    # =====================================================
    # Degree Centrality
    # =====================================================

    def degree_centrality(self):
        """
        Compute Degree Centrality.
        """

        logger.info(
            "Running Degree Centrality..."
        )

        query = """
        CALL gds.degree.write(

            $graph_name,

            {
                writeProperty: 'degree'
            }

        )

        YIELD nodePropertiesWritten
        """

        result = self.neo4j.execute_query(
            query,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )

        logger.info(
            "Degree written to %s nodes.",
            result[0]["nodePropertiesWritten"],
        )

    # =====================================================
    # Betweenness Centrality
    # =====================================================

    def betweenness_centrality(self):
        """
        Compute Betweenness Centrality.
        """

        logger.info(
            "Running Betweenness..."
        )

        query = """
        CALL gds.betweenness.write(

            $graph_name,

            {
                writeProperty: 'betweenness'
            }

        )

        YIELD nodePropertiesWritten
        """

        result = self.neo4j.execute_query(
            query,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )

        logger.info(
            "Betweenness written to %s nodes.",
            result[0]["nodePropertiesWritten"],
        )

    # =====================================================
    # Top Degree Nodes
    # =====================================================

    def top_degree_nodes(
        self,
        limit: int = 20,
    ):
        """
        Return highest degree nodes.
        """

        query = """
        MATCH (e:Entity)

        RETURN

            e.name AS name,
            e.entity_type AS type,
            e.degree AS degree

        ORDER BY degree DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Top Betweenness Nodes
    # =====================================================

    def top_betweenness_nodes(
        self,
        limit: int = 20,
    ):
        """
        Return highest betweenness nodes.
        """

        query = """
        MATCH (e:Entity)

        RETURN

            e.name AS name,
            e.entity_type AS type,
            e.betweenness AS betweenness

        ORDER BY betweenness DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )
    # =====================================================
    # Top Closeness Nodes
    # =====================================================
    
    def top_closeness_nodes(
        self,
        limit: int = 20,
    ):
        """
        Return highest closeness nodes.
        """
    
        query = """
        MATCH (e:Entity)
    
        RETURN
    
            e.name AS name,
            e.entity_type AS type,
            e.closeness AS closeness
    
        ORDER BY closeness DESC
    
        LIMIT $limit
        """
    
        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Cleanup
    # =====================================================

    def drop_projection(self):
        """
        Remove graph projection.
        """

        self.neo4j.execute_query(
            """
            CALL gds.graph.drop(
                $graph_name,
                false
            )
            """,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )

        logger.info(
            "Projection removed."
        )

    def close(self):

        self.neo4j.close()
        
    # =====================================================
    # Closeness Centrality
    # =====================================================
    
    def closeness_centrality(self):
        """
        Compute Closeness Centrality.
        """
    
        logger.info(
            "Running Closeness Centrality..."
        )
    
        query = """
        CALL gds.closeness.write(
    
            $graph_name,
    
            {
                writeProperty: 'closeness'
            }
    
        )
    
        YIELD nodePropertiesWritten
        """
    
        result = self.neo4j.execute_query(
            query,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )
    
        logger.info(
            "Closeness written to %s nodes.",
            result[0]["nodePropertiesWritten"],
        )
        
    # =====================================================
    # Louvain Community Detection
    # =====================================================
    
    def louvain_communities(self):
        """
        Detect graph communities using Louvain.
        """
    
        logger.info(
            "Running Louvain Community Detection..."
        )
    
        query = """
        CALL gds.louvain.write(
    
            $graph_name,
    
            {
                writeProperty: 'community'
            }
    
        )
    
        YIELD communityCount,
              nodePropertiesWritten
        """
    
        result = self.neo4j.execute_query(
            query,
            {
                "graph_name": self.GRAPH_NAME,
            },
        )
    
        logger.info(
            "Detected %s communities.",
            result[0]["communityCount"],
        )
    
        logger.info(
            "Community written to %s nodes.",
            result[0]["nodePropertiesWritten"],
        )
    # =====================================================
    # Largest Communities
    # =====================================================
    
    def largest_communities(self):
        """
        Return detected communities.
        """
    
        query = """
        MATCH (e:Entity)
    
        RETURN
    
            e.community AS community,
            count(*) AS nodes
    
        ORDER BY nodes DESC
        """
    
        return self.neo4j.execute_query(query)