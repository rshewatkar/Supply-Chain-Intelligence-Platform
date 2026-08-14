from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class RiskScoreEngine:
    """
    Supply-chain risk scoring engine.

    Combines:
    - Supplier dependency
    - Country dependency
    - Tier-1 dependency
    - Tier-2 dependency

    into an overall entity risk score.
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =========================================================
    # Risk Weights
    # =========================================================

    SUPPLIER_WEIGHT = 0.35
    COUNTRY_WEIGHT = 0.20
    TIER1_WEIGHT = 0.25
    TIER2_WEIGHT = 0.20

    # =========================================================
    # Risk Levels
    # =========================================================

    def assign_risk_level(self, score: float) -> str:
        """
        Convert risk score into a risk level.
        """

        if score >= 0.75:
            return "CRITICAL"

        if score >= 0.50:
            return "HIGH"

        if score >= 0.25:
            return "MEDIUM"

        return "LOW"

    # =========================================================
    # Calculate Risk Score
    # =========================================================

    def calculate_risk_score(
        self,
        supplier_dependency: float,
        country_dependency: float,
        tier1_dependency: float,
        tier2_dependency: float,
    ) -> float:
        """
        Calculate weighted overall risk score.
        """

        score = (
            supplier_dependency * self.SUPPLIER_WEIGHT
            + country_dependency * self.COUNTRY_WEIGHT
            + tier1_dependency * self.TIER1_WEIGHT
            + tier2_dependency * self.TIER2_WEIGHT
        )

        return round(score, 4)

    # =========================================================
    # Calculate Entity Risk
    # =========================================================

    def calculate_entity_risk(
        self,
        supplier_dependency: float,
        country_dependency: float,
        tier1_dependency: float,
        tier2_dependency: float,
    ) -> dict:
        """
        Calculate complete risk result for one entity.
        """

        score = self.calculate_risk_score(
            supplier_dependency=supplier_dependency,
            country_dependency=country_dependency,
            tier1_dependency=tier1_dependency,
            tier2_dependency=tier2_dependency,
        )

        risk_level = self.assign_risk_level(score)

        return {
            "supplier_dependency": supplier_dependency,
            "country_dependency": country_dependency,
            "tier1_dependency": tier1_dependency,
            "tier2_dependency": tier2_dependency,
            "risk_score": score,
            "risk_level": risk_level,
        }

    # =========================================================
    # Read Existing Dependency Metrics
    # =========================================================

    def get_entity_dependency_metrics(
        self,
        entity_name: str,
    ):
        """
        Retrieve dependency metrics for an entity.

        The query is intentionally kept separate from the
        scoring logic so the scoring engine can be changed
        without changing the database layer.
        """

        query = """
        MATCH (e:Entity {name: $entity_name})

        RETURN
            e.name AS entity,
            coalesce(e.supplier_dependency, 0.0)
                AS supplier_dependency,
            coalesce(e.country_dependency, 0.0)
                AS country_dependency,
            coalesce(e.tier1_dependency, 0.0)
                AS tier1_dependency,
            coalesce(e.tier2_dependency, 0.0)
                AS tier2_dependency
        """

        return self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
            },
        )

    # =========================================================
    # Save Risk Score
    # =========================================================

    def save_risk_score(
        self,
        entity_name: str,
        risk_result: dict,
    ):
        """
        Save calculated risk metrics to Neo4j.
        """

        query = """
        MATCH (e:Entity {name: $entity_name})

        SET
            e.supplier_dependency =
                $supplier_dependency,

            e.country_dependency =
                $country_dependency,

            e.tier1_dependency =
                $tier1_dependency,

            e.tier2_dependency =
                $tier2_dependency,

            e.risk_score =
                $risk_score,

            e.risk_level =
                $risk_level

        RETURN
            e.name AS entity,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level
        """

        result = self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
                **risk_result,
            },
        )

        logger.info(
            "Risk score saved for %s.",
            entity_name,
        )

        return result

    # =========================================================
    # Calculate and Save
    # =========================================================

    def calculate_and_save(
        self,
        entity_name: str,
    ):
        """
        Calculate risk score from stored dependency metrics
        and save the result to Neo4j.
        """

        logger.info(
            "Calculating risk score for %s...",
            entity_name,
        )

        metrics = self.get_entity_dependency_metrics(
            entity_name
        )

        if not metrics:
            logger.warning(
                "No dependency metrics found for %s.",
                entity_name,
            )

            return None

        data = metrics[0]

        risk_result = self.calculate_entity_risk(
            supplier_dependency=float(
                data["supplier_dependency"]
            ),
            country_dependency=float(
                data["country_dependency"]
            ),
            tier1_dependency=float(
                data["tier1_dependency"]
            ),
            tier2_dependency=float(
                data["tier2_dependency"]
            ),
        )

        self.save_risk_score(
            entity_name,
            risk_result,
        )

        return {
            "entity": entity_name,
            **risk_result,
        }

    # =========================================================
    # Top Risky Entities
    # =========================================================

    def top_risky_entities(
        self,
        limit: int = 20,
    ):
        """
        Return entities with the highest risk scores.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.name AS entity,
            e.entity_type AS type,
            e.supplier_dependency AS supplier_dependency,
            e.country_dependency AS country_dependency,
            e.tier1_dependency AS tier1_dependency,
            e.tier2_dependency AS tier2_dependency,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =========================================================
    # Close
    # =========================================================

    def close(self):
        """
        Close Neo4j connection.
        """

        self.neo4j.close()