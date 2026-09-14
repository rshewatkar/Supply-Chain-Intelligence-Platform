"""
Graph Analytics Page - Knowledge Graph Visualization & Analysis

Displays graph statistics, entity distributions, centrality metrics,
risk distributions, and community structures from Neo4j.
All data is fetched live from Neo4j using DashboardQueries.
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


def render_header() -> None:
    """Render page header and introduction."""
    st.title("Graph Analytics")
    st.markdown(
        "Explore your supply chain knowledge graph, including entities, "
        "relationships, centrality metrics, risk distributions, and communities."
    )
    st.divider()


def render_summary_metrics(queries: DashboardQueries) -> None:
    """Render high-level graph statistics."""
    try:
        summary = queries.get_summary()
        st.subheader("Graph Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Entities", f"{summary.get('total_entities', 0):,}",
                      help="Total nodes in the knowledge graph")
        with col2:
            st.metric("Relationships", f"{summary.get('total_relationships', 0):,}",
                      help="Total connections in the graph")
        with col3:
            st.metric("Communities", f"{summary.get('total_communities', 0):,}",
                      help="Detected supply chain communities")
    except Exception as e:
        logger.error(f"Error rendering summary metrics: {e}")
        st.error("Unable to load graph summary.")


def render_entity_type_distribution(queries: DashboardQueries) -> None:
    """Render entity type distribution chart and table."""
    try:
        distribution = queries.get_entity_type_distribution()
        if not distribution:
            st.info("No entity type data available yet.")
            return
        df = pd.DataFrame(distribution)
        st.subheader("Entity Type Distribution")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df.set_index("type")["total"], use_container_width=True)
        with col2:
            st.dataframe(
                df.rename(columns={"type": "Type", "total": "Count"}),
                use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"Error rendering entity type distribution: {e}")
        st.warning("Unable to load entity type distribution.")


def render_top_degree_entities(queries: DashboardQueries) -> None:
    """Render entities with highest degree centrality."""
    try:
        entities = queries.get_top_degree_entities(limit=20)
        if not entities:
            st.info("No degree centrality data available yet.")
            return
        st.subheader("Top Degree Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(columns={"name": "Name", "type": "Type", "degree": "Degree"}),
            use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"Error rendering degree centrality: {e}")
        st.warning("Unable to load degree centrality data.")


def render_top_betweenness_entities(queries: DashboardQueries) -> None:
    """Render entities with highest betweenness centrality."""
    try:
        entities = queries.get_top_betweenness_entities(limit=20)
        if not entities:
            st.info("No betweenness centrality data available yet.")
            return
        st.subheader("Top Betweenness Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(columns={"name": "Name", "type": "Type", "betweenness": "Betweenness"}),
            use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"Error rendering betweenness centrality: {e}")
        st.warning("Unable to load betweenness centrality data.")


def render_top_closeness_entities(queries: DashboardQueries) -> None:
    """Render entities with highest closeness centrality."""
    try:
        entities = queries.get_top_closeness_entities(limit=20)
        if not entities:
            st.info("No closeness centrality data available yet.")
            return
        st.subheader("Top Closeness Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(columns={"name": "Name", "type": "Type", "closeness": "Closeness"}),
            use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"Error rendering closeness centrality: {e}")
        st.warning("Unable to load closeness centrality data.")
