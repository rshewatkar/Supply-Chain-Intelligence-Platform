from app.graph.neo4j_manager import Neo4jManager
from app.utils.logger import get_logger

logger = get_logger(__name__)

class RiskScoring:
    """
    Computer supplier risk scores using graph analytics metrics.
    
    uses:
    - Degree Centrality
    - Betweenness Centrality
    - Closeness Centrality
    
    Saves:
    - risk_scores
    - risk_level
    
    """
    
    def __init__(self):
        self.neo4j = Neo4jManager()
    
    # =====================================================
    # Normalize Metrics
    # =====================================================
    
    def normalize_metrics(self):
        """
        Normalize the graph analytics metrics to a 0-1 scale.
        """
        
        logger.info("Normalizing graph analytics metrics...")
        
        query = """
        MATCH (e:Entity)
        
        with
            
            max(e.degree) As maxDegree,
            max(e.betweenness) As maxBetweenness,
            max(e.closeness) As maxCloseness
        
        MATCH (n:Entity)
        
        SET
            n.degree_norm = 
            CASE 
                WHEN maxDegree = 0 THEN 0
                ELSE n.degree / maxDegree
            END,
            
            n.betweenness_norm =
            CASE
                WHEN maxBetweenness = 0 THEN 0
                ELSE n.betweenness / maxBetweenness
            END,
            
            n.closeness_norm =
            CASE
                WHEN maxCloseness = 0 THEN 0
                ELSE n.closeness / maxCloseness
            END
            
            """
        self.neo4j.execute_query(query)
        
    # =====================================================
    # Compute Risk Scores
    # =====================================================
    
    def compute_risk_scores(self):
        """
        Compute weighted supplier risk score.
        
        """
        
        logger.info("Computing risk scores...")
        
        query = """
        MATCH (e:Entity)
        
        SET
            e.risk_score =
                (0.40 * coalesce(e.degree_norm, 0)) +
                (0.40 * coalesce(e.betweenness_norm, 0)) +
                (0.20 * coalesce(e.closeness_norm, 0))
        """
        
        self.neo4j.execute_query(query)
        
        logger.info("Risk scores computed successfully.")
        
    # =====================================================
    # Risk Level
    # =====================================================
    
    def assign_risk_levels(self):
        """
        Assign business-friendly risk labels.
        
        """
        
        logger.info("Assigning risk levels...")
        
        query = """
        MATCH (e:Entity)
        
        SET
        
        e.risk_level = 
        
        CASE    
        
            WHEN e.risk_score >= 0.75 THEN 'CRITICAL'
            WHEN e.risk_score >= 0.50 THEN 'HIGH'
            WHEN e.risk_score >= 0.25 THEN 'MEDIUM'
            ELSE 'LOW'
        
        END
        
        """
        
        self.neo4j.execute_query(query)
        
        logger.info("Risk levels assigned successfully.")
        
    # =====================================================
    # Top Risk Nodes
    # =====================================================
    
    def top_risky_entities(
        self,
        limit: int = 20,
    ):
        """
        Return highest risk entities.
        """
        
                
        query = """
        MATCH (e:Entity)
        
        RETURN
            e.name AS name,
            e.entity_type AS type,
            round(e.risk_score,4) AS risk_score,
            e.risk_level AS risk_level,
            e.degree As degree,
            e.betweenness As betweenness,
            e.closeness As closeness
                    
        ORDER BY
            risk_score DESC
        
        LIMIT $limit
        """
        
        return self.neo4j.execute_query(
            query,
            {
                "limit": limit,
            },
        )
        
                
        
    #=====================================================
    # RUN
    #=====================================================
    
    def run(self):
        
        self.normalize_metrics()
        self.compute_risk_scores()
        self.assign_risk_levels()
        
        logger.info("Risk scoring completed successfully.")
    
    def close(self):
        """
        Close Neo4j connection.
        """
        
        self.neo4j.close()
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
                
                
        
        
        
        
        
        
        
        
        
        
        
        
        
            

        