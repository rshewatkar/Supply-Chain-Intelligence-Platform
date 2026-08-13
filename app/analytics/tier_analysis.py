from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class TierAnalysis:
    """
    Analyze Tier-1 and Tier-2 supply-chain relationships.

    Tier-1:
        Direct relationship from a company to another entity.

    Tier-2:
        Entity reached through two relationship hops.

    The analysis uses the existing Neo4j graph and dynamic
    relationship types.
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =====================================================
    # Tier-1 Analysis
    # =====================================================

    def get_tier_1_dependencies(self, company_name):
        """
        Return direct dependencies of a company.

        Tier-1 = one-hop relationships.
        """

        logger.info(
            "Calculating Tier-1 dependencies for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r]->(dependency:Entity)

        RETURN
            company.name AS company,
            dependency.name AS dependency,
            dependency.entity_type AS dependency_type,
            type(r) AS relationship_type,
            coalesce(r.occurrence_count, 1) AS occurrence_count

        ORDER BY occurrence_count DESC, dependency.name
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
            },
        )

    # =====================================================
    # Tier-2 Analysis
    # =====================================================

    def get_tier_2_dependencies(self, company_name):
        """
        Return indirect dependencies of a company.

        Tier-2 = two-hop relationships.

        Direct Tier-1 entities are excluded from the result.
        """

        logger.info(
            "Calculating Tier-2 dependencies for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r1]->(tier1:Entity)-[r2]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        RETURN DISTINCT
            company.name AS company,
            tier1.name AS tier_1_entity,
            tier1.entity_type AS tier_1_type,
            tier2.name AS tier_2_entity,
            tier2.entity_type AS tier_2_type,
            type(r1) AS tier_1_relationship,
            type(r2) AS tier_2_relationship

        ORDER BY tier_2_entity
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
            },
        )

    # =====================================================
    # Tier Summary
    # =====================================================

    def get_tier_summary(self, company_name):
        """
        Return Tier-1 and Tier-2 dependency counts.
        """

        logger.info(
            "Generating tier summary for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {
            name: $company_name
        })

        OPTIONAL MATCH (company)-[]->(tier1:Entity)

        WITH company, count(DISTINCT tier1) AS tier1_count

        OPTIONAL MATCH (company)-[]->(t1:Entity)-[]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        RETURN
            company.name AS company,
            tier1_count AS tier_1_dependencies,
            count(DISTINCT tier2) AS tier_2_dependencies
        """

        result = self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
            },
        )

        return result

    # =====================================================
    # Highest Exposure Tier-1 Entities
    # =====================================================

    def top_tier_1_dependencies(
        self,
        company_name,
        limit=20,
    ):
        """
        Return the most frequently occurring Tier-1
        dependencies.
        """

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r]->(dependency:Entity)

        RETURN
            dependency.name AS dependency,
            dependency.entity_type AS type,
            type(r) AS relationship_type,
            coalesce(r.occurrence_count, 1) AS occurrence_count

        ORDER BY occurrence_count DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
                "limit": limit,
            },
        )

    # =====================================================
    # Highest Exposure Tier-2 Entities
    # =====================================================

    def top_tier_2_dependencies(
        self,
        company_name,
        limit=20,
    ):
        """
        Return the most relevant Tier-2 dependencies.
        """

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r1]->(tier1:Entity)-[r2]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        RETURN DISTINCT
            tier2.name AS dependency,
            tier2.entity_type AS type,
            tier1.name AS through_entity,
            type(r1) AS tier_1_relationship,
            type(r2) AS tier_2_relationship

        ORDER BY dependency

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
                "limit": limit,
            },
        )

    # =====================================================
    # Run Analysis
    # =====================================================

    def run(self, company_name):
        """
        Run complete Tier-1 / Tier-2 analysis.
        """

        logger.info(
            "Starting Tier-1 / Tier-2 analysis for %s...",
            company_name,
        )

        tier_1 = self.get_tier_1_dependencies(
            company_name
        )

        tier_2 = self.get_tier_2_dependencies(
            company_name
        )

        summary = self.get_tier_summary(
            company_name
        )

        logger.info(
            "Tier analysis completed for %s.",
            company_name,
        )

        return {
            "summary": summary,
            "tier_1": tier_1,
            "tier_2": tier_2,
        }

    # =====================================================
    # Close
    # =====================================================

    def close(self):
        self.neo4j.close()