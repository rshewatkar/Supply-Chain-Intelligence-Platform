from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class RiskDashboardBackend:
    """
    Backend data provider for the Risk Dashboard.

    This class retrieves risk metrics already calculated and
    persisted in Neo4j by the analytics/risk engines.

    It does NOT calculate risk again.
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =========================================================
    # Risk Overview
    # =========================================================

    def get_risk_overview(self):
        """
        Return overall risk statistics.
        """

        query = """
        MATCH (e:Entity)

        RETURN
            count(e) AS total_entities,

            count(
                CASE
                    WHEN e.risk_level = 'CRITICAL'
                    THEN 1
                END
            ) AS critical_entities,

            count(
                CASE
                    WHEN e.risk_level = 'HIGH'
                    THEN 1
                END
            ) AS high_entities,

            count(
                CASE
                    WHEN e.risk_level = 'MEDIUM'
                    THEN 1
                END
            ) AS medium_entities,

            count(
                CASE
                    WHEN e.risk_level = 'LOW'
                    THEN 1
                END
            ) AS low_entities,

            coalesce(avg(e.risk_score), 0.0)
                AS average_risk_score,

            coalesce(max(e.risk_score), 0.0)
                AS maximum_risk_score
        """

        result = self.neo4j.execute_query(query)

        return result[0] if result else {}

    # =========================================================
    # Top Risky Entities
    # =========================================================

    def get_top_risky_entities(self, limit=20):
        """
        Return entities with the highest risk scores.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.name AS entity,
            e.entity_type AS type,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level,
            coalesce(e.supplier_dependency, 0.0)
                AS supplier_dependency,
            coalesce(e.country_dependency, 0.0)
                AS country_dependency,
            coalesce(e.tier1_dependency, 0.0)
                AS tier1_dependency,
            coalesce(e.tier2_dependency, 0.0)
                AS tier2_dependency,
            coalesce(e.degree, 0.0)
                AS degree,
            coalesce(e.betweenness, 0.0)
                AS betweenness,
            coalesce(e.closeness, 0.0)
                AS closeness

        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =========================================================
    # Risk Distribution
    # =========================================================

    def get_risk_distribution(self):
        """
        Return number of entities by risk level.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_level IS NOT NULL

        RETURN
            e.risk_level AS risk_level,
            count(e) AS total

        ORDER BY
            CASE e.risk_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
                ELSE 5
            END
        """

        return self.neo4j.execute_query(query)

    # =========================================================
    # Risk By Entity Type
    # =========================================================

    def get_risk_by_entity_type(self):
        """
        Return average and maximum risk by entity type.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.entity_type AS type,
            count(e) AS total_entities,
            round(avg(e.risk_score) * 1000) / 1000.0
                AS average_risk,
            round(max(e.risk_score) * 1000) / 1000.0
                AS maximum_risk

        ORDER BY average_risk DESC
        """

        return self.neo4j.execute_query(query)

    # =========================================================
    # Dependency Risk
    # =========================================================

    def get_dependency_risk(self, limit=20):
        """
        Return entities with their dependency metrics.

        Useful for identifying what is contributing to risk.
        """

        query = """
        MATCH (e:Entity)

        WHERE
            e.risk_score IS NOT NULL
            AND (
                e.supplier_dependency IS NOT NULL
                OR e.country_dependency IS NOT NULL
                OR e.tier1_dependency IS NOT NULL
                OR e.tier2_dependency IS NOT NULL
            )

        RETURN
            e.name AS entity,
            e.entity_type AS type,

            coalesce(e.supplier_dependency, 0.0)
                AS supplier_dependency,

            coalesce(e.country_dependency, 0.0)
                AS country_dependency,

            coalesce(e.tier1_dependency, 0.0)
                AS tier1_dependency,

            coalesce(e.tier2_dependency, 0.0)
                AS tier2_dependency,

            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =========================================================
    # Centrality Risk
    # =========================================================

    def get_centrality_risk(self, limit=20):
        """
        Return entities combining graph centrality and risk.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.name AS entity,
            e.entity_type AS type,
            coalesce(e.degree, 0.0) AS degree,
            coalesce(e.betweenness, 0.0)
                AS betweenness,
            coalesce(e.closeness, 0.0)
                AS closeness,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =========================================================
    # Entity Risk Details
    # =========================================================

    def get_entity_risk(self, entity_name):
        """
        Return complete risk information for one entity.
        """

        query = """
        MATCH (e:Entity {
            name: $entity_name
        })

        RETURN
            e.name AS entity,
            e.entity_type AS type,

            coalesce(e.supplier_dependency, 0.0)
                AS supplier_dependency,

            coalesce(e.country_dependency, 0.0)
                AS country_dependency,

            coalesce(e.tier1_dependency, 0.0)
                AS tier1_dependency,

            coalesce(e.tier2_dependency, 0.0)
                AS tier2_dependency,

            coalesce(e.degree, 0.0)
                AS degree,

            coalesce(e.betweenness, 0.0)
                AS betweenness,

            coalesce(e.closeness, 0.0)
                AS closeness,

            coalesce(e.risk_score, 0.0)
                AS risk_score,

            coalesce(e.risk_level, 'UNKNOWN')
                AS risk_level
        """

        return self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
            },
        )

    # =========================================================
    # High Risk Entities
    # =========================================================

    def get_high_risk_entities(self, limit=20):
        """
        Return HIGH and CRITICAL risk entities.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_level IN ['CRITICAL', 'HIGH']

        RETURN
            e.name AS entity,
            e.entity_type AS type,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level,
            coalesce(e.supplier_dependency, 0.0)
                AS supplier_dependency,
            coalesce(e.country_dependency, 0.0)
                AS country_dependency,
            coalesce(e.tier1_dependency, 0.0)
                AS tier1_dependency,
            coalesce(e.tier2_dependency, 0.0)
                AS tier2_dependency

        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =========================================================
    # Dashboard Data
    # =========================================================

    def get_dashboard_data(self, limit=20):
        """
        Return all major datasets required by the dashboard.
        """

        logger.info(
            "Loading risk dashboard data..."
        )

        data = {
            "overview": self.get_risk_overview(),

            "top_risky_entities":
                self.get_top_risky_entities(limit),

            "risk_distribution":
                self.get_risk_distribution(),

            "risk_by_entity_type":
                self.get_risk_by_entity_type(),

            "dependency_risk":
                self.get_dependency_risk(limit),

            "centrality_risk":
                self.get_centrality_risk(limit),

            "high_risk_entities":
                self.get_high_risk_entities(limit),
        }

        logger.info(
            "Risk dashboard data loaded successfully."
        )

        return data

    # =========================================================
    # Close
    # =========================================================

    def close(self):
        """
        Close Neo4j connection.
        """

        self.neo4j.close()