from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class SupplierDependency:
    """
    Calculates supplier dependency metrics for Entity nodes.

    Supplier dependency is based on supplier/customer-related
    relationships in the Neo4j graph.

    The resulting metric is written back to each Entity node
    as:

        supplier_dependency

    Value range:

        0.0 -> 1.0
    """

    SUPPLIER_RELATIONSHIP_TYPES = (
        "SUPPLIES_TO",
        "SUPPLIES",
        "CUSTOMER_OF",
    )

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =========================================================
    # Calculate Supplier Dependency
    # =========================================================

    def calculate_supplier_dependency(self):
        """
        Calculate supplier dependency for every Entity.

        Formula:

            supplier_dependency =
                supplier_relationships / total_relationships

        Entities without relationships receive 0.0.
        """

        logger.info(
            "Calculating supplier dependency..."
        )

        query = """
        MATCH (e:Entity)

        OPTIONAL MATCH (e)-[r]-()

        WITH
            e,
            count(r) AS total_relationships,
            count(
                CASE
                    WHEN type(r) IN [
                        "SUPPLIES_TO",
                        "SUPPLIES",
                        "CUSTOMER_OF"
                    ]
                    THEN r
                END
            ) AS supplier_relationships

        WITH
            e,
            total_relationships,
            supplier_relationships,
            CASE
                WHEN total_relationships = 0
                THEN 0.0
                ELSE
                    toFloat(supplier_relationships)
                    / total_relationships
            END AS supplier_dependency

        SET
            e.supplier_dependency = supplier_dependency

        RETURN
            e.name AS name,
            e.entity_type AS type,
            total_relationships,
            supplier_relationships,
            supplier_dependency

        ORDER BY supplier_dependency DESC
        """

        result = self.neo4j.execute_query(query)

        logger.info(
            "Supplier dependency calculated for %s entities.",
            len(result),
        )

        return result

    # =========================================================
    # Top Supplier-Dependent Entities
    # =========================================================

    def top_supplier_dependent_entities(
        self,
        limit: int = 20,
    ):
        """
        Return entities with the highest supplier dependency.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.supplier_dependency IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.supplier_dependency AS supplier_dependency,
            e.degree AS degree,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY supplier_dependency DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =========================================================
    # Supplier Dependency Summary
    # =========================================================

    def dependency_summary(self):
        """
        Return a summary of supplier dependency levels.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.supplier_dependency IS NOT NULL

        RETURN

            count(e) AS total_entities,

            count(
                CASE
                    WHEN e.supplier_dependency >= 0.75
                    THEN 1
                END
            ) AS very_high_dependency,

            count(
                CASE
                    WHEN e.supplier_dependency >= 0.50
                     AND e.supplier_dependency < 0.75
                    THEN 1
                END
            ) AS high_dependency,

            count(
                CASE
                    WHEN e.supplier_dependency >= 0.25
                     AND e.supplier_dependency < 0.50
                    THEN 1
                END
            ) AS medium_dependency,

            count(
                CASE
                    WHEN e.supplier_dependency < 0.25
                    THEN 1
                END
            ) AS low_dependency
        """

        result = self.neo4j.execute_query(query)

        return result[0] if result else {}

    # =========================================================
    # Run
    # =========================================================

    def run(self):
        """
        Execute the complete supplier dependency analysis.
        """

        logger.info(
            "Starting supplier dependency analysis..."
        )

        self.calculate_supplier_dependency()

        summary = self.dependency_summary()

        top_entities = (
            self.top_supplier_dependent_entities()
        )

        logger.info(
            "Supplier dependency analysis completed."
        )

        return {
            "summary": summary,
            "top_entities": top_entities,
        }

    # =========================================================
    # Close
    # =========================================================

    def close(self):
        """
        Close Neo4j connection.
        """

        self.neo4j.close()