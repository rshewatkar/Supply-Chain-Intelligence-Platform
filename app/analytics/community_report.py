from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class CommunityReport:
    """
    Generate supply-chain community analytics reports.

    Uses Louvain community assignments and graph/risk
    metrics already stored in Neo4j.

    Provides:
    - Community summary
    - Community members
    - Community risk analysis
    - Top communities
    - Community relationship analysis
    """

    def __init__(self):

        self.neo4j = Neo4jManager()

    # =====================================================
    # Community Summary
    # =====================================================

    def community_summary(self):
        """
        Return a summary of all detected communities.
        """

        logger.info(
            "Generating community summary..."
        )

        query = """
        MATCH (e:Entity)

        WHERE e.community IS NOT NULL

        RETURN
            e.community AS community,
            count(e) AS node_count,
            avg(e.risk_score) AS average_risk,
            max(e.risk_score) AS maximum_risk

        ORDER BY average_risk DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Community Members
    # =====================================================

    def community_members(
        self,
        community_id,
    ):
        """
        Return entities belonging to a community.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.community = $community_id

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.degree AS degree,
            e.betweenness AS betweenness,
            e.closeness AS closeness,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY risk_score DESC
        """

        return self.neo4j.execute_query(
            query,
            {
                "community_id": community_id,
            },
        )

    # =====================================================
    # Community Risk
    # =====================================================

    def community_risk(self):
        """
        Rank communities by their risk.
        """

        logger.info(
            "Calculating community risk..."
        )

        query = """
        MATCH (e:Entity)

        WHERE
            e.community IS NOT NULL
            AND e.risk_score IS NOT NULL

        RETURN
            e.community AS community,
            count(e) AS node_count,
            avg(e.risk_score) AS average_risk,
            max(e.risk_score) AS maximum_risk,
            sum(
                CASE
                    WHEN e.risk_level = 'CRITICAL'
                    THEN 1
                    ELSE 0
                END
            ) AS critical_nodes,
            sum(
                CASE
                    WHEN e.risk_level = 'HIGH'
                    THEN 1
                    ELSE 0
                END
            ) AS high_risk_nodes

        ORDER BY average_risk DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Top Communities
    # =====================================================

    def top_communities(
        self,
        limit: int = 10,
    ):
        """
        Return the largest communities.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.community IS NOT NULL

        RETURN
            e.community AS community,
            count(e) AS node_count,
            avg(e.degree) AS average_degree,
            avg(e.risk_score) AS average_risk

        ORDER BY node_count DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Community Relationships
    # =====================================================

    def community_relationships(
        self,
        community_id,
    ):
        """
        Return relationships occurring inside a community.
        """

        query = """
        MATCH
            (a:Entity)-[r]->(b:Entity)

        WHERE
            a.community = $community_id
            AND b.community = $community_id

        RETURN
            type(r) AS relationship_type,
            count(r) AS relationship_count

        ORDER BY relationship_count DESC
        """

        return self.neo4j.execute_query(
            query,
            {
                "community_id": community_id,
            },
        )

    # =====================================================
    # Community Risk Leaders
    # =====================================================

    def highest_risk_entities_by_community(
        self,
        limit: int = 5,
    ):
        """
        Return the highest-risk entities from each community.
        """

        query = """
        MATCH (e:Entity)

        WHERE
            e.community IS NOT NULL
            AND e.risk_score IS NOT NULL

        WITH
            e.community AS community,
            e

        ORDER BY
            community,
            e.risk_score DESC

        WITH
            community,
            collect({
                name: e.name,
                type: e.entity_type,
                risk_score: e.risk_score,
                risk_level: e.risk_level
            })[0..$limit] AS entities

        RETURN
            community,
            entities

        ORDER BY community
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Full Report
    # =====================================================

    def run(self):
        """
        Generate the complete community analytics report.
        """

        logger.info(
            "Starting community analytics report..."
        )

        summary = self.community_summary()

        risk = self.community_risk()

        top = self.top_communities()

        logger.info(
            "Community analytics report completed."
        )

        return {
            "summary": summary,
            "risk": risk,
            "top_communities": top,
        }

    # =====================================================
    # Close
    # =====================================================

    def close(self):

        self.neo4j.close()