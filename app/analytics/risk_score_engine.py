from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class RiskScoreEngine:
    """
    Calculate supply-chain risk scores using graph analytics
    and dependency metrics.

    Metrics used:

        - Degree centrality
        - Betweenness centrality
        - Closeness centrality
        - Supplier dependency
        - Country dependency
        - Tier-1 dependency
        - Tier-2 dependency

    Final risk score range:

        0.0 -> 1.0
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

        # =====================================================
        # Risk Weights
        # =====================================================

        self.weights = {
            "degree": 0.20,
            "betweenness": 0.20,
            "closeness": 0.10,
            "supplier_dependency": 0.20,
            "country_dependency": 0.10,
            "tier1_dependency": 0.10,
            "tier2_dependency": 0.10,
        }

    # =========================================================
    # Load Metrics
    # =========================================================

    def load_metrics(self):
        """
        Load all risk-related metrics from Neo4j.

        Tier dependency metrics are expected to already be
        persisted by TierAnalysis.
        """

        logger.info(
            "Loading risk metrics from Neo4j..."
        )

        query = """
        MATCH (e:Entity)

        RETURN
            e.name AS name,
            e.entity_type AS entity_type,

            coalesce(e.degree, 0.0) AS degree,
            coalesce(e.betweenness, 0.0) AS betweenness,
            coalesce(e.closeness, 0.0) AS closeness,

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
            ) AS tier2_dependency_count
        """

        results = self.neo4j.execute_query(query)

        logger.info(
            "Loaded metrics for %s entities.",
            len(results),
        )

        return results

    # =========================================================
    # Normalize Metrics
    # =========================================================

    def normalize_metrics(self, metrics):
        """
        Normalize graph metrics using min-max normalization.

        Dependency metrics are already expected to be in
        the 0-1 range, so they are preserved.
        """

        if not metrics:
            return []

        metric_fields = [
            "degree",
            "betweenness",
            "closeness",
        ]

        normalized = []

        for row in metrics:

            item = dict(row)

            for field in metric_fields:

                values = [
                    float(r.get(field) or 0.0)
                    for r in metrics
                ]

                minimum = min(values)
                maximum = max(values)

                value = float(
                    row.get(field) or 0.0
                )

                if maximum == minimum:
                    normalized_value = 0.0
                else:
                    normalized_value = (
                        value - minimum
                    ) / (
                        maximum - minimum
                    )

                item[f"{field}_normalized"] = (
                    normalized_value
                )

            # Dependency metrics are already 0-1.

            dependency_fields = [
                "supplier_dependency",
                "country_dependency",
                "tier1_dependency",
                "tier2_dependency",
            ]

            for field in dependency_fields:

                value = float(
                    row.get(field) or 0.0
                )

                item[f"{field}_normalized"] = max(
                    0.0,
                    min(1.0, value),
                )

            normalized.append(item)

        return normalized

    # =========================================================
    # Compute Risk Score
    # =========================================================

    def compute_risk_scores(self, metrics):
        """
        Calculate weighted risk score.

        Formula:

            risk_score =
                degree * 0.20
                + betweenness * 0.20
                + closeness * 0.10
                + supplier_dependency * 0.20
                + country_dependency * 0.10
                + tier1_dependency * 0.10
                + tier2_dependency * 0.10
        """

        logger.info(
            "Computing risk scores..."
        )

        results = []

        for row in metrics:

            degree = row[
                "degree_normalized"
            ]

            betweenness = row[
                "betweenness_normalized"
            ]

            closeness = row[
                "closeness_normalized"
            ]

            supplier_dependency = row[
                "supplier_dependency_normalized"
            ]

            country_dependency = row[
                "country_dependency_normalized"
            ]

            tier1_dependency = row[
                "tier1_dependency_normalized"
            ]

            tier2_dependency = row[
                "tier2_dependency_normalized"
            ]

            risk_score = (
                degree
                * self.weights["degree"]
                +
                betweenness
                * self.weights["betweenness"]
                +
                closeness
                * self.weights["closeness"]
                +
                supplier_dependency
                * self.weights[
                    "supplier_dependency"
                ]
                +
                country_dependency
                * self.weights[
                    "country_dependency"
                ]
                +
                tier1_dependency
                * self.weights[
                    "tier1_dependency"
                ]
                +
                tier2_dependency
                * self.weights[
                    "tier2_dependency"
                ]
            )

            item = dict(row)

            item["risk_score"] = round(
                risk_score,
                4,
            )

            results.append(item)

        logger.info(
            "Risk scores calculated for %s entities.",
            len(results),
        )

        return results

    # =========================================================
    # Assign Risk Levels
    # =========================================================

    def assign_risk_levels(self, results):
        """
        Assign LOW / MEDIUM / HIGH / CRITICAL levels.
        """

        for row in results:

            score = row["risk_score"]

            if score >= 0.75:
                level = "CRITICAL"

            elif score >= 0.50:
                level = "HIGH"

            elif score >= 0.25:
                level = "MEDIUM"

            else:
                level = "LOW"

            row["risk_level"] = level

        return results

    # =========================================================
    # Save Risk Metrics
    # =========================================================

    def save_risk_scores(self, results):
        """
        Persist risk metrics and final risk score to Neo4j.
        """

        logger.info(
            "Saving risk scores to Neo4j..."
        )

        query = """
        UNWIND $rows AS row

        MATCH (e:Entity {
            name: row.name
        })

        SET
            e.risk_score = row.risk_score,
            e.risk_level = row.risk_level

        RETURN count(e) AS updated_entities
        """

        rows = [
            {
                "name": row["name"],
                "risk_score": row["risk_score"],
                "risk_level": row["risk_level"],
            }
            for row in results
        ]

        result = self.neo4j.execute_query(
            query,
            {
                "rows": rows,
            },
        )

        logger.info(
            "Risk scores saved to Neo4j."
        )

        return result

    # =========================================================
    # Top Risky Entities
    # =========================================================

    def top_risky_entities(self, limit=20):
        """
        Return entities with the highest risk scores.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS entity_type,

            e.risk_score AS risk_score,
            e.risk_level AS risk_level,

            e.degree AS degree,
            e.betweenness AS betweenness,
            e.closeness AS closeness,

            e.supplier_dependency
                AS supplier_dependency,

            e.country_dependency
                AS country_dependency,

            e.tier1_dependency
                AS tier1_dependency,

            e.tier2_dependency
                AS tier2_dependency,

            e.tier1_dependency_count
                AS tier1_dependency_count,

            e.tier2_dependency_count
                AS tier2_dependency_count

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
    # Run
    # =========================================================

    def run(self):
        """
        Execute complete risk scoring pipeline.
        """

        logger.info(
            "Starting Risk Score Engine..."
        )

        metrics = self.load_metrics()

        normalized = self.normalize_metrics(
            metrics
        )

        scores = self.compute_risk_scores(
            normalized
        )

        scored = self.assign_risk_levels(
            scores
        )

        self.save_risk_scores(
            scored
        )

        top_entities = (
            self.top_risky_entities()
        )

        logger.info(
            "Risk Score Engine completed."
        )

        return {
            "results": scored,
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