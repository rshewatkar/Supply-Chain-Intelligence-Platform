"""
Home Page - Supply Chain Intelligence Platform Overview

Displays real-time platform metrics and navigation to key features.
All metrics are fetched live from Neo4j using DashboardQueries.
"""

import streamlit as st
import pandas as pd
from app.dashboard.dashboard_queries import DashboardQueries
from app.utils.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def get_queries():
    """Get cached DashboardQueries instance."""
    return DashboardQueries()


def render_header():
    """Render page header and introduction."""
    st.title("🏠 Supply Chain Intelligence Platform")
    st.markdown(
        "Welcome to your supply chain intelligence hub. Monitor entities, "
        "relationships, dependencies, risk metrics, and graph analytics in real-time."
    )
    st.divider()


def render_summary_metrics(queries):
    """Render KPI metrics from Neo4j."""
    try:
        summary = queries.get_summary()
        st.subheader("📊 Platform Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Entities", f"{summary.get('total_entities', 0):,}", 
                     help="Total nodes in knowledge graph")
        with col2:
            st.metric("Relationships", f"{summary.get('total_relationships', 0):,}",
                     help="Total connections in graph")
        with col3:
            st.metric("Communities", f"{summary.get('total_communities', 0):,}",
                     help="Detected supply chain communities")
        with col4:
            st.metric("Status", "Active", help="Platform operational status")
    except Exception as e:
        logger.error(f"Error rendering summary metrics: {e}")
        st.error("Unable to load platform metrics.")


def render_entity_distribution(queries):
    """Render entity type distribution chart."""
    try:
        distribution = queries.get_entity_type_distribution()
        if not distribution:
            st.info("No entity data available yet.")
            return
        
        df = pd.DataFrame(distribution)
        st.subheader("📈 Entity Type Distribution")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df.set_index("type")["total"], use_container_width=True)
        with col2:
            st.dataframe(
                df.rename(columns={"type": "Type", "total": "Count"}),
                use_container_width=True, hide_index=True
            )
    except Exception as e:
        logger.error(f"Error rendering entity distribution: {e}")
        st.warning("Unable to load entity distribution.")


def render_relationship_distribution(queries):
    """Render relationship type distribution chart."""
    try:
        distribution = queries.get_relationship_distribution()
        if not distribution:
            st.info("No relationship data available yet.")
            return
        
        df = pd.DataFrame(distribution)
        st.subheader("🔗 Relationship Distribution")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df.set_index("relationship_type")["total"], 
                        use_container_width=True)
        with col2:
            st.dataframe(
                df.rename(columns={"relationship_type": "Type", "total": "Count"}),
                use_container_width=True, hide_index=True
            )
    except Exception as e:
        logger.error(f"Error rendering relationship distribution: {e}")
        st.warning("Unable to load relationship distribution.")


def render_feature_cards():
    """Render navigation cards to dashboard features."""
    st.divider()
    st.subheader("🚀 Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("**📊 Graph Analysis**\n\nExplore networks, centrality metrics, "
               "and communities.")
    with col2:
        st.info("**⚠️ Risk Analytics**\n\nMonitor risk scores and dependencies.")
    with col3:
        st.info("**🏢 Companies**\n\nSearch and analyze companies.")
    with col4:
        st.info("**🤖 AI Assistant**\n\nAsk natural language questions.")


def render_platform_info():
    """Render platform information and capabilities."""
    st.divider()
    st.subheader("ℹ️ About This Platform")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            **Core Capabilities**
            - Knowledge Graph mapping of supply chains
            - Real-time risk scoring and dependency analysis
            - Graph centrality and community detection
            - Natural language Q&A with RAG
            - Entity relationship exploration
            - Multi-tier supply chain analysis
        """)
    
    with col2:
        st.markdown("""
            **Technology Stack**
            - **Neo4j** - Knowledge Graph database
            - **Qdrant** - Vector embeddings
            - **FastAPI** - Backend analytics
            - **Streamlit** - Interactive dashboard
            - **LangChain** - RAG pipeline
            - **Graph Data Science** - Centrality metrics
        """)


def render_footer():
    """Render page footer."""
    st.divider()
    st.caption("Supply Chain Intelligence Platform | "
              "Real-time Neo4j + Graph Analytics + Risk Intelligence")


def main() -> None:
    """Render the Home page."""
    queries = get_queries()
    
    render_header()
    render_summary_metrics(queries)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        render_entity_distribution(queries)
    with col2:
        render_relationship_distribution(queries)
    
    render_feature_cards()
    render_platform_info()
    render_footer()
