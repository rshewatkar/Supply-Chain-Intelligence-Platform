from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class CountryDependency:
    """
    Analyze country dependency within the supply-chain graph.

    Country dependency is measured using the number of
    supply-chain entities connected to each country.
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =====================================================
    # Country Dependency
    # =====================================================

    def calculate_country_dependency(self):
        """
        Calculate dependency metrics for each country.

        Returns:
            List of dictionaries containing:
            - country
            - connected_entities
            - total_relationships
            - dependency_score
        """

        logger.info("Calculating country dependency...")

        query = """
        MATCH (country:Entity)
        WHERE country.entity_type = 'COUNTRY'

        OPTIONAL MATCH (country)-[r]-(entity:Entity)
        WHERE entity.entity_type <> 'COUNTRY'

        WITH
            country,
            count(DISTINCT entity) AS connected_entities,
            count(r) AS total_relationships

        WITH
            country,
            connected_entities,
            total_relationships,
            CASE
                WHEN total_relationships = 0 THEN 0.0
                ELSE 
                    toFloat(connected_entities) / total_relationships
            END AS dependency_score
        
        SET country.country_dependency = dependency_score

        RETURN
            country.name AS country,
            connected_entities,
            total_relationships,
            dependency_score

        ORDER BY dependency_score DESC
        """

        results = self.neo4j.execute_query(query)

        logger.info(
            "Calculated dependency for %s countries.",
            len(results),
        )

        return results

    # =====================================================
    # Top Countries
    # =====================================================

    def top_dependency_countries(self, limit: int = 10):
        """
        Return countries with the highest dependency.
        """

        logger.info(
            "Finding top %s dependency countries...",
            limit,
        )

        query = """
        MATCH (country:Entity)
        
        WHERE 
             country.entity_type = 'COUNTRY'
             AND country.country_dependency IS NOT NULL    

        RETURN
            country.name AS country,
            country.country_dependency AS country_dependency,
            country.degree AS degree,
            country.betweenness AS betweenness,
            country.closeness AS closeness,
            country.risk_score AS risk_score,
            country.risk_level AS risk_level

        ORDER BY country_dependency DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Country Risk
    # =====================================================

    def country_dependency_risk(self, limit: int = 10):
        """
        Identify countries with high supply-chain dependency.

        Risk levels are based on relationship concentration.
        """

        query = """
        MATCH (country:Entity)
        WHERE country.entity_type = 'COUNTRY'

        OPTIONAL MATCH (country)-[r]-(entity:Entity)
        WHERE entity.entity_type <> 'COUNTRY'

        WITH
            country,
            count(DISTINCT entity) AS connected_entities,
            count(r) AS total_relationships

        WITH
            country,
            connected_entities,
            total_relationships,
            CASE
                WHEN total_relationships >= 50
                    THEN 'HIGH'
                WHEN total_relationships >= 20
                    THEN 'MEDIUM'
                ELSE 'LOW'
            END AS risk_level

        RETURN
            country.name AS country,
            connected_entities,
            total_relationships,
            risk_level

        ORDER BY total_relationships DESC
        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Run
    # =====================================================

    def run(self):
        """
        Execute country dependency analysis.
        """

        logger.info(
            "Starting country dependency analysis..."
        )

        dependency = self.calculate_country_dependency()

        logger.info(
            "Country dependency analysis completed."
        )

        return dependency

    # =====================================================
    # Close
    # =====================================================

    def close(self):
        self.neo4j.close()