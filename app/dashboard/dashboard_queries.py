from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DashboardQueries:
    """
    Read-only Neo4j queries used by the Graph Analytics Dashboard.

    This class does not calculate analytics.
    It only retrieves metrics already stored in Neo4j.
    """

    def __init__(self):
        self.neo4j = Neo4jManager()

    # =====================================================
    # Dashboard Summary
    # =====================================================

    def get_summary(self):
        """
        Return high-level graph statistics.
        """

        query = """
        MATCH (e:Entity)
        OPTIONAL MATCH ()-[r]->()

        RETURN
            count(DISTINCT e) AS total_entities,
            count(DISTINCT r) AS total_relationships,
            count(DISTINCT e.community) AS total_communities
        """

        result = self.neo4j.execute_query(query)

        if not result:
            return {
                "total_entities": 0,
                "total_relationships": 0,
                "total_communities": 0,
            }

        return result[0]

    # =====================================================
    # Entity Type Distribution
    # =====================================================

    def get_entity_type_distribution(self):
        """
        Return number of entities by entity type.
        """

        query = """
        MATCH (e:Entity)

        RETURN
            e.entity_type AS type,
            count(e) AS total

        ORDER BY total DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Relationship Distribution
    # =====================================================

    def get_relationship_distribution(self):
        """
        Return number of relationships by relationship type.
        """

        query = """
        MATCH ()-[r]->()

        RETURN
            type(r) AS relationship_type,
            count(r) AS total

        ORDER BY total DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Top Degree Entities
    # =====================================================

    def get_top_degree_entities(self, limit=20):
        """
        Return entities with highest degree centrality.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.degree IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.degree AS degree

        ORDER BY e.degree DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =====================================================
    # Top Betweenness Entities
    # =====================================================

    def get_top_betweenness_entities(self, limit=20):
        """
        Return entities with highest betweenness centrality.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.betweenness IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.betweenness AS betweenness

        ORDER BY e.betweenness DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =====================================================
    # Top Closeness Entities
    # =====================================================

    def get_top_closeness_entities(self, limit=20):
        """
        Return entities with highest closeness centrality.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.closeness IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.closeness AS closeness

        ORDER BY e.closeness DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =====================================================
    # Highest Risk Entities
    # =====================================================

    def get_top_risk_entities(self, limit=20):
        """
        Return entities with highest risk scores.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.risk_score IS NOT NULL

        RETURN
            e.name AS name,
            e.entity_type AS type,
    
            e.risk_score AS risk_score,
            e.risk_level AS risk_level,
    
            e.supplier_dependency AS supplier_dependency,
            e.country_dependency AS country_dependency,
            e.tier1_dependency AS tier1_dependency,
            e.tier2_dependency AS tier2_dependency,
    
            e.degree AS degree,
            e.betweenness AS betweenness,
            e.closeness AS closeness,
            e.community AS community
        
        ORDER BY e.risk_score DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {"limit": limit},
        )

    # =====================================================
    # Risk Level Distribution
    # =====================================================

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

        ORDER BY total DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Community Summary
    # =====================================================

    def get_community_summary(self):
        """
        Return community-level statistics.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.community IS NOT NULL

        RETURN
            e.community AS community,
            count(e) AS nodes,
            avg(e.risk_score) AS avg_risk,
            max(e.risk_score) AS max_risk,
            avg(e.degree) AS avg_degree

        ORDER BY avg_risk DESC
        """

        return self.neo4j.execute_query(query)

    # =====================================================
    # Community Members
    # =====================================================

    def get_community_members(self, community):
        """
        Return entities belonging to a specific community.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.community = $community

        RETURN
            e.name AS name,
            e.entity_type AS type,
            e.degree AS degree,
            e.betweenness AS betweenness,
            e.closeness AS closeness,
            e.risk_score AS risk_score,
            e.risk_level AS risk_level

        ORDER BY e.risk_score DESC
        """

        return self.neo4j.execute_query(
            query,
            {
                "community": community,
            },
        )

    # =====================================================
    # Graph Relationships
    # =====================================================

    def get_graph_data(self, limit=100):
        """
        Return nodes and relationships for graph visualization.

        Used by the interactive graph view.
        """

        query = """
        MATCH (source:Entity)-[r]->(target:Entity)

        RETURN
            source.entity_id AS source_id,
            source.name AS source,
            source.entity_type AS source_type,

            target.entity_id AS target_id,
            target.name AS target,
            target.entity_type AS target_type,

            type(r) AS relationship_type,
            coalesce(r.occurrence_count, 1) AS weight

        ORDER BY weight DESC

        LIMIT $limit
        """

        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )

    # =====================================================
    # Entity Details
    # =====================================================

    def get_entity_details(self, entity_name):
        """
        Return detailed analytics for a selected entity.
        """

        query = """
        MATCH (e:Entity)

        WHERE e.name = $entity_name

        RETURN
            e.name AS name,
            e.entity_type AS type,
    
            e.degree AS degree,
            e.betweenness AS betweenness,
            e.closeness AS closeness,
            e.community AS community,
    
            e.supplier_dependency AS supplier_dependency,
            e.country_dependency AS country_dependency,
            e.tier1_dependency AS tier1_dependency,
            e.tier2_dependency AS tier2_dependency,
    
            e.risk_score AS risk_score,
            e.risk_level AS risk_level
            
        """

        return self.neo4j.execute_query(
            query,
            {
                "entity_name": entity_name,
            },
        )
    
    # =====================================================
    # Risk Dependency Metrics
    # =====================================================
    
    def get_risk_dependency_metrics(self, limit=20):
        """
        Return dependency metrics used by the Risk Dashboard.
        """
    
        query = """
        MATCH (e:Entity)
    
        WHERE e.risk_score IS NOT NULL
    
        RETURN
            e.name AS name,
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

    # =====================================================
    # Close Connection
    # =====================================================

    def close(self):
        self.neo4j.close()