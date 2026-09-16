"""
Graph Analytics Page - Knowledge Graph Visualization & Analysis

Displays graph statistics, entity distributions, centrality metrics,
risk distributions, community structures, entity explorer, and raw
graph relationships from Neo4j.

All data is fetched live from Neo4j using DashboardQueries.
"""

import streamlit as st
import pandas as pd
from app.dashboard.dashboard_queries import DashboardQueries
from app.utils.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def get_queries() -> DashboardQueries:
    """Get cached DashboardQueries instance."""
    return DashboardQueries()


# =========================================================
# Sidebar Controls
# =========================================================


def render_sidebar_controls() -> dict:
    """Render sidebar controls and return user-selected parameters.

    Returns
    -------
    dict
        Keys: ``top_n`` (int) and ``graph_limit`` (int).
    """
    st.sidebar.header("Graph Controls")

    top_n: int = st.sidebar.slider(
        "Number of entities",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Controls how many entities appear in centrality / risk tables.",
    )

    graph_limit: int = st.sidebar.slider(
        "Graph relationships",
        min_value=20,
        max_value=300,
        value=100,
        step=20,
        help="Maximum relationships shown in the Graph Relationships table.",
    )

    return {"top_n": top_n, "graph_limit": graph_limit}


# =========================================================
# Header
# =========================================================


def render_header() -> None:
    """Render page header and introduction."""
    st.title("📊 Graph Analytics")
    st.markdown(
        "Explore your supply chain knowledge graph, including entities, "
        "relationships, centrality metrics, risk distributions, communities, "
        "and raw graph data."
    )
    st.divider()


# =========================================================
# Summary Metrics
# =========================================================


def render_summary_metrics(queries: DashboardQueries) -> None:
    """Render high-level graph statistics."""
    try:
        summary = queries.get_summary()
        st.subheader("🔢 Graph Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Entities",
                f"{summary.get('total_entities', 0):,}",
                help="Total nodes in the knowledge graph",
            )
        with col2:
            st.metric(
                "Relationships",
                f"{summary.get('total_relationships', 0):,}",
                help="Total connections in the graph",
            )
        with col3:
            st.metric(
                "Communities",
                f"{summary.get('total_communities', 0):,}",
                help="Detected supply chain communities",
            )
    except Exception as e:
        logger.error(f"Error rendering summary metrics: {e}")
        st.error("Unable to load graph summary.")


# =========================================================
# Entity Type Distribution
# =========================================================


def render_entity_type_distribution(queries: DashboardQueries) -> None:
    """Render entity type distribution chart and table."""
    try:
        distribution = queries.get_entity_type_distribution()
        if not distribution:
            st.info("No entity type data available yet.")
            return
        df = pd.DataFrame(distribution)
        st.subheader("📦 Entity Type Distribution")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df.set_index("type")["total"], use_container_width=True)
        with col2:
            st.dataframe(
                df.rename(columns={"type": "Type", "total": "Count"}),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as e:
        logger.error(f"Error rendering entity type distribution: {e}")
        st.warning("Unable to load entity type distribution.")


# =========================================================
# Relationship Distribution
# =========================================================


def render_relationship_distribution(queries: DashboardQueries) -> None:
    """Render relationship type distribution chart and table."""
    try:
        distribution = queries.get_relationship_distribution()
        if not distribution:
            st.info("No relationship data available yet.")
            return
        df = pd.DataFrame(distribution)
        st.subheader("🔗 Relationship Distribution")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(
                df.set_index("relationship_type")["total"],
                use_container_width=True,
            )
        with col2:
            st.dataframe(
                df.rename(columns={"relationship_type": "Type", "total": "Count"}),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as e:
        logger.error(f"Error rendering relationship distribution: {e}")
        st.warning("Unable to load relationship distribution.")


# =========================================================
# Centrality Metrics
# =========================================================


def render_top_degree_entities(queries: DashboardQueries, limit: int = 20) -> None:
    """Render entities with highest degree centrality."""
    try:
        entities = queries.get_top_degree_entities(limit=limit)
        if not entities:
            st.info("No degree centrality data available yet.")
            return
        st.subheader("🎯 Top Degree Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(columns={"name": "Name", "type": "Type", "degree": "Degree"}),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        logger.error(f"Error rendering degree centrality: {e}")
        st.warning("Unable to load degree centrality data.")


def render_top_betweenness_entities(
    queries: DashboardQueries, limit: int = 20
) -> None:
    """Render entities with highest betweenness centrality."""
    try:
        entities = queries.get_top_betweenness_entities(limit=limit)
        if not entities:
            st.info("No betweenness centrality data available yet.")
            return
        st.subheader("🔀 Top Betweenness Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(
                columns={
                    "name": "Name",
                    "type": "Type",
                    "betweenness": "Betweenness",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        logger.error(f"Error rendering betweenness centrality: {e}")
        st.warning("Unable to load betweenness centrality data.")


def render_top_closeness_entities(
    queries: DashboardQueries, limit: int = 20
) -> None:
    """Render entities with highest closeness centrality."""
    try:
        entities = queries.get_top_closeness_entities(limit=limit)
        if not entities:
            st.info("No closeness centrality data available yet.")
            return
        st.subheader("📍 Top Closeness Centrality")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(
                columns={"name": "Name", "type": "Type", "closeness": "Closeness"}
            ),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        logger.error(f"Error rendering closeness centrality: {e}")
        st.warning("Unable to load closeness centrality data.")


# =========================================================
# Risk Distribution
# =========================================================


def render_risk_distribution(queries: DashboardQueries) -> None:
    """Render risk level distribution chart and table."""
    try:
        distribution = queries.get_risk_distribution()
        if not distribution:
            st.info("No risk distribution data available yet.")
            return
        df = pd.DataFrame(distribution)
        st.subheader("⚠️ Risk Level Distribution")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(
                df.set_index("risk_level")["total"], use_container_width=True
            )
        with col2:
            st.dataframe(
                df.rename(columns={"risk_level": "Risk Level", "total": "Count"}),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as e:
        logger.error(f"Error rendering risk distribution: {e}")
        st.warning("Unable to load risk distribution.")


# =========================================================
# Top Risk Entities
# =========================================================


def render_top_risk_entities(queries: DashboardQueries, limit: int = 20) -> None:
    """Render entities with the highest risk scores."""
    try:
        entities = queries.get_top_risk_entities(limit=limit)
        if not entities:
            st.info("No risk entity data available yet.")
            return
        st.subheader("🚨 Top Risk Entities")
        df = pd.DataFrame(entities)
        st.dataframe(
            df.rename(
                columns={
                    "name": "Name",
                    "type": "Type",
                    "risk_score": "Risk Score",
                    "risk_level": "Risk Level",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as e:
        logger.error(f"Error rendering top risk entities: {e}")
        st.warning("Unable to load top risk entities.")


# =========================================================
# Community Summary
# =========================================================


def render_community_summary(queries: DashboardQueries) -> None:
    """Render community-level statistics and average risk bar chart."""
    try:
        summary = queries.get_community_summary()
        if not summary:
            st.info("No community data available yet.")
            return
        st.subheader("🏘️ Community Summary")
        df = pd.DataFrame(summary)
        st.dataframe(
            df.rename(
                columns={
                    "community": "Community",
                    "nodes": "Nodes",
                    "avg_risk": "Avg Risk",
                    "max_risk": "Max Risk",
                    "avg_degree": "Avg Degree",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        # Community average risk bar chart
        if {"community", "avg_risk"}.issubset(df.columns):
            st.markdown("**Community Average Risk**")
            st.bar_chart(
                df.set_index("community")["avg_risk"], use_container_width=True
            )
    except Exception as e:
        logger.error(f"Error rendering community summary: {e}")
        st.warning("Unable to load community summary.")


# =========================================================
# Community Explorer
# =========================================================


def render_community_explorer(queries: DashboardQueries) -> None:
    """Explore members of a specific community."""
    try:
        st.subheader("🔎 Community Explorer")
        community_summary = queries.get_community_summary()
        if not community_summary:
            st.info("No community data available to explore.")
            return
        communities = [c["community"] for c in community_summary]
        selected_community = st.selectbox(
            "Select a community:",
            options=communities,
            key="graph_community_selector",
        )
        if selected_community is not None:
            members = queries.get_community_members(selected_community)
            if members:
                df = pd.DataFrame(members)
                st.markdown(
                    f"**Community {selected_community}** — {len(members)} members"
                )
                st.dataframe(
                    df.rename(
                        columns={
                            "name": "Name",
                            "type": "Type",
                            "degree": "Degree",
                            "betweenness": "Betweenness",
                            "closeness": "Closeness",
                            "risk_score": "Risk Score",
                            "risk_level": "Risk Level",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(f"No members found in Community {selected_community}.")
    except Exception as e:
        logger.error(f"Error rendering community explorer: {e}")
        st.warning("Unable to load community explorer data.")


# =========================================================
# Entity Explorer
# =========================================================


def render_entity_explorer(queries: DashboardQueries, limit: int = 100) -> None:
    """Provide a searchable entity detail viewer.

    Retrieves the top risk entities as selectable options and displays
    full details (as JSON) for the chosen entity.
    """
    try:
        st.subheader("🧩 Entity Explorer")
        entity_names = [
            row["name"]
            for row in queries.get_top_risk_entities(limit)
            if row.get("name")
        ]
        if not entity_names:
            st.info("No entities available for exploration.")
            return
        selected_entity = st.selectbox(
            "Select an entity:",
            options=entity_names,
            key="graph_entity_selector",
        )
        if selected_entity:
            entity_details = queries.get_entity_details(selected_entity)
            if entity_details:
                st.json(entity_details[0])
            else:
                st.info(f"No details found for entity '{selected_entity}'.")
    except Exception as e:
        logger.error(f"Error rendering entity explorer: {e}")
        st.warning("Unable to load entity explorer data.")


# =========================================================
# Graph Relationships
# =========================================================


def render_graph_relationships(queries: DashboardQueries, limit: int = 100) -> None:
    """Render a table of raw graph relationships."""
    try:
        st.subheader("🗺️ Graph Relationships")
        graph_data = queries.get_graph_data(limit)
        if not graph_data:
            st.info("No graph relationship data available yet.")
            return
        df = pd.DataFrame(graph_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"Error rendering graph relationships: {e}")
        st.warning("Unable to load graph relationship data.")


# =========================================================
# Footer
# =========================================================


def render_footer() -> None:
    """Render page footer."""
    st.divider()
    st.caption(
        "Supply Chain Intelligence Platform | "
        "Neo4j + Graph Data Science + Risk Analytics"
    )


# =========================================================
# Main
# =========================================================


def main() -> None:
    """Render the Graph Analytics page."""
    try:
        queries = get_queries()
        controls = render_sidebar_controls()
        top_n: int = controls["top_n"]
        graph_limit: int = controls["graph_limit"]

        render_header()
        render_summary_metrics(queries)
        st.divider()

        # Entity and Relationship Distributions
        col1, col2 = st.columns(2)
        with col1:
            render_entity_type_distribution(queries)
        with col2:
            render_relationship_distribution(queries)

        st.divider()

        # Centrality Metrics
        render_top_degree_entities(queries, limit=top_n)
        st.divider()
        render_top_betweenness_entities(queries, limit=top_n)
        st.divider()
        render_top_closeness_entities(queries, limit=top_n)
        st.divider()

        # Risk
        render_risk_distribution(queries)
        st.divider()
        render_top_risk_entities(queries, limit=top_n)
        st.divider()

        # Communities
        render_community_summary(queries)
        st.divider()
        render_community_explorer(queries)
        st.divider()

        # Entity Explorer
        render_entity_explorer(queries)
        st.divider()

        # Graph Relationships (raw data)
        render_graph_relationships(queries, limit=graph_limit)

        render_footer()

    except Exception as e:
        logger.error(f"Error rendering graph analytics page: {e}")
        st.error("An error occurred while rendering the graph analytics page.")


if __name__ == "__main__":
    main()
