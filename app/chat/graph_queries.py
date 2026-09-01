from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class GraphQueries:
    """
    Neo4j query layer for the AI Supply Chain Assistant.

    Provides graph queries for:

    - Suppliers
    - Common suppliers
    - Dependency metrics
    - Tier-2 dependencies
    - Supply-chain relationships
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =====================================================
    # Suppliers
    # =====================================================

    def get_suppliers(
        self,
        company_name: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Return entities that are suppliers to a company.
        Filters by entity type 'COMPANY' and relevant supply-chain relationships.
        """

        logger.info(
            "Fetching suppliers for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {name: $company_name})-[r]-(supplier:Entity)
        WHERE supplier <> company
          AND supplier.entity_type = 'COMPANY'
          AND type(r) IN ['SUPPLIES', 'DEPENDS_ON', 'PART_OF']

        RETURN DISTINCT
            supplier.name AS supplier,
            supplier.entity_type AS supplier_type,
            collect(type(r)) AS relationship_types,
            sum(coalesce(r.occurrence_count, 1)) AS total_occurrence_count

        ORDER BY total_occurrence_count DESC,
                 supplier
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
    # Common Suppliers
    # =====================================================

    def get_common_suppliers(
        self,
        company_1: str,
        company_2: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Return entities connected to both companies.

        Useful for questions such as:

        - Which suppliers are common between Apple and NVIDIA?
        - What suppliers do AMD and Intel share?
        """

        logger.info(
            "Finding common suppliers between %s and %s...",
            company_1,
            company_2,
        )

        query = """
        MATCH (company1:Entity {
            name: $company_1
        })-[r1]-(supplier:Entity)-[r2]-(company2:Entity {
            name: $company_2
        })

        WHERE supplier <> company1
          AND supplier <> company2
          AND company1 <> company2

        RETURN DISTINCT
            supplier.name AS supplier,
            supplier.entity_type AS supplier_type,
            type(r1) AS company_1_relationship,
            type(r2) AS company_2_relationship,
            coalesce(
                r1.occurrence_count,
                1
            ) +
            coalesce(
                r2.occurrence_count,
                1
            ) AS relationship_strength

        ORDER BY relationship_strength DESC,
                 supplier

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "company_1": company_1,
                "company_2": company_2,
                "limit": limit,
            },
        )

    # =====================================================
    # Dependency Metrics
    # =====================================================

    def get_dependency_metrics(
        self,
        entity_name: str,
    ) -> list[dict]:
        """
        Return dependency and risk metrics for an entity.

        Metrics are read from values already calculated
        and persisted by the analytics pipeline.
        """

        logger.info(
            "Fetching dependency metrics for %s...",
            entity_name,
        )

        query = """
        MATCH (e:Entity {
            name: $entity_name
        })

        RETURN
            e.name AS entity,
            e.entity_type AS entity_type,

            coalesce(
                e.supplier_dependency,
                0.0
            ) AS supplier_dependency,

            coalesce(
                e.country_dependency,
                0.0
            ) AS country_dependency,

            coalesce(
                e.tier1_dependency,
                0.0
            ) AS tier1_dependency,

            coalesce(
                e.tier2_dependency,
                0.0
            ) AS tier2_dependency,

            coalesce(
                e.tier1_dependency_count,
                0
            ) AS tier1_dependency_count,

            coalesce(
                e.tier2_dependency_count,
                0
            ) AS tier2_dependency_count,

            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        LIMIT 1
        """

        return self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
            },
        )

    # =====================================================
    # Tier-2 Dependencies
    # =====================================================

    def get_tier_2_dependencies(
        self,
        company_name: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Return indirect Tier-2 dependencies.

        Tier-2 entities are reached through two
        relationship hops.

        Direct dependencies are excluded.
        """

        logger.info(
            "Fetching Tier-2 dependencies for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r1]->(tier1:Entity)-[r2]->(tier2:Entity)

        WHERE tier2 <> company
          AND NOT (company)-[]->(tier2)

        RETURN DISTINCT
            tier2.name AS dependency,
            tier2.entity_type AS dependency_type,
            tier1.name AS through_entity,
            tier1.entity_type AS through_entity_type,
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
    # Tier-1 Dependencies
    # =====================================================

    def get_tier_1_dependencies(
        self,
        company_name: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Return direct Tier-1 dependencies.
        """

        logger.info(
            "Fetching Tier-1 dependencies for %s...",
            company_name,
        )

        query = """
        MATCH (company:Entity {
            name: $company_name
        })-[r]->(dependency:Entity)

        RETURN
            dependency.name AS dependency,
            dependency.entity_type AS dependency_type,
            type(r) AS relationship_type,
            coalesce(
                r.occurrence_count,
                1
            ) AS occurrence_count

        ORDER BY occurrence_count DESC,
                 dependency

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
    # Supply Chain Relationships
    # =====================================================

    def get_supply_chain_relationships(
        self,
        entity_name: str,
        limit: int = 30,
    ) -> list[dict]:
        """
        Return direct supply-chain relationships
        connected to an entity.
        """

        logger.info(
            "Fetching supply-chain relationships for %s...",
            entity_name,
        )

        query = """
        MATCH (entity:Entity {
            name: $entity_name
        })-[r]-(connected:Entity)

        RETURN
            entity.name AS entity,
            entity.entity_type AS entity_type,
            connected.name AS connected_entity,
            connected.entity_type AS connected_type,
            type(r) AS relationship_type,
            coalesce(
                r.occurrence_count,
                1
            ) AS occurrence_count

        ORDER BY occurrence_count DESC,
                 connected_entity

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
                "limit": limit,
            },
        )

    # =====================================================
    # Entity Search
    # =====================================================

    def find_entities(
        self,
        search_term: str,
        limit: int = 10,
    ) -> list[dict]:
        """
        Find entities by name.

        This helper will later be useful for extracting
        company names from user questions.
        """

        query = """
        MATCH (e:Entity)

        WHERE toLower(e.name)
              CONTAINS toLower($search_term)

        RETURN
            e.name AS name,
            e.entity_type AS entity_type

        ORDER BY e.name

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "search_term": search_term,
                "limit": limit,
            },
        )

    # =====================================================
    # Close Connection
    # =====================================================

    def close(self):
        """
        Close the Neo4j connection.
        """

        logger.info(
            "Closing GraphQueries Neo4j connection."
        )

        self.neo4j.close()