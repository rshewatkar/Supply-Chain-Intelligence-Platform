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

    Dependency metrics are persisted on COMPANY nodes:

        tier1_dependency_count
        tier2_dependency_count
        tier1_dependency
        tier2_dependency

    The dependency scores are normalized between 0.0 and 1.0.
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

        Direct Tier-1 entities are excluded.
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
    # Tier Summary - Single Company
    # =====================================================

    def get_tier_summary(self, company_name):
        """
        Return Tier-1 and Tier-2 dependency counts
        for one company.
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

        WITH
            company,
            count(DISTINCT tier1) AS tier1_count

        OPTIONAL MATCH
            (company)-[]->(tier1_entity:Entity)-[]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        WITH
            company,
            tier1_count,
            count(DISTINCT tier2) AS tier2_count

        RETURN
            company.name AS company,
            tier1_count AS tier_1_dependencies,
            tier2_count AS tier_2_dependencies
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_name": company_name,
            },
        )

    # =====================================================
    # Calculate Metrics - ALL Companies
    # =====================================================

    def calculate_dependency_metrics(self):
        """
        Calculate Tier-1 and Tier-2 dependency metrics
        for every COMPANY node.

        Metrics written to Neo4j:

            tier1_dependency_count
            tier2_dependency_count

            tier1_dependency
            tier2_dependency

        Formula:

            total_dependencies =
                tier1_count + tier2_count

            tier1_dependency =
                tier1_count / total_dependencies

            tier2_dependency =
                tier2_count / total_dependencies

        Companies with no dependencies receive:

            tier1_dependency = 0.0
            tier2_dependency = 0.0
        """

        logger.info(
            "Calculating Tier-1 / Tier-2 dependency metrics "
            "for all companies..."
        )

        query = """
        MATCH (company:Entity)
        WHERE company.entity_type = 'COMPANY'

        // -------------------------------------------------
        // Tier-1
        // -------------------------------------------------

        OPTIONAL MATCH
            (company)-[]->(tier1:Entity)

        WITH
            company,
            count(DISTINCT tier1) AS tier1_count

        // -------------------------------------------------
        // Tier-2
        // -------------------------------------------------

        OPTIONAL MATCH
            (company)-[]->(tier1_entity:Entity)-[]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        WITH
            company,
            tier1_count,
            count(DISTINCT tier2) AS tier2_count

        // -------------------------------------------------
        // Total dependency count
        // -------------------------------------------------

        WITH
            company,
            tier1_count,
            tier2_count,
            tier1_count + tier2_count AS total_dependencies

        // -------------------------------------------------
        // Normalized metrics
        // -------------------------------------------------

        WITH
            company,
            tier1_count,
            tier2_count,
            total_dependencies,

            CASE
                WHEN total_dependencies = 0
                THEN 0.0
                ELSE
                    toFloat(tier1_count)
                    / total_dependencies
            END AS tier1_dependency,

            CASE
                WHEN total_dependencies = 0
                THEN 0.0
                ELSE
                    toFloat(tier2_count)
                    / total_dependencies
            END AS tier2_dependency

        // -------------------------------------------------
        // Persist metrics
        // -------------------------------------------------

        SET
            company.tier1_dependency_count = tier1_count,
            company.tier2_dependency_count = tier2_count,

            company.tier1_dependency = tier1_dependency,
            company.tier2_dependency = tier2_dependency

        RETURN
            company.name AS company,

            tier1_count AS tier_1_dependencies,
            tier2_count AS tier_2_dependencies,

            total_dependencies,

            tier1_dependency,
            tier2_dependency

        ORDER BY tier1_dependency DESC
        """

        results = self.neo4j.execute_query(query)

        logger.info(
            "Tier dependency metrics calculated for %s companies.",
            len(results),
        )

        return results

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
    # Tier Dependency Summary - ALL Companies
    # =====================================================

    def dependency_summary(self):
        """
        Return Tier-1 / Tier-2 metrics for all companies.
        """

        query = """
        MATCH (company:Entity)
        WHERE company.entity_type = 'COMPANY'

        RETURN
            company.name AS company,

            company.tier1_dependency_count
                AS tier_1_dependencies,

            company.tier2_dependency_count
                AS tier_2_dependencies,

            company.tier1_dependency
                AS tier1_dependency,

            company.tier2_dependency
                AS tier2_dependency

        ORDER BY tier1_dependency DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Run Analysis
    # =====================================================

    def run(self, company_name=None):
        """
        Run Tier-1 / Tier-2 analysis.

        If company_name is provided:
            Run detailed analysis for that company.

        Regardless of company_name:
            Calculate and persist dependency metrics
            for ALL companies.
        """

        logger.info(
            "Starting Tier-1 / Tier-2 analysis..."
        )

        # -------------------------------------------------
        # Calculate metrics for ALL companies
        # -------------------------------------------------

        metrics = self.calculate_dependency_metrics()

        result = {
            "metrics": metrics,
        }

        # -------------------------------------------------
        # Optional detailed company analysis
        # -------------------------------------------------

        if company_name:

            logger.info(
                "Running detailed analysis for %s...",
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

            result.update(
                {
                    "summary": summary,
                    "tier_1": tier_1,
                    "tier_2": tier_2,
                }
            )

        logger.info(
            "Tier analysis completed."
        )

        return result

    # =====================================================
    # Close
    # =====================================================

    def close(self):
        self.neo4j.close()