import pandas as pd
import streamlit as st

from app.dashboard.dashboard_queries import DashboardQueries

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Supply Chain Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# Helpers
# =========================================================

@st.cache_resource
def get_queries():
    return DashboardQueries()


queries = get_queries()


# =========================================================
# Header
# =========================================================

st.title("Supply Chain Intelligence Platform")

st.markdown(
    """
    ### Graph Analytics Dashboard

    Explore supply-chain entities, relationships,
    graph centrality, communities, and risk metrics.
    """
)


# =========================================================
# Sidebar
# =========================================================

st.sidebar.header("Dashboard Controls")

top_n = st.sidebar.slider(
    "Number of entities",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
)

graph_limit = st.sidebar.slider(
    "Graph relationships",
    min_value=20,
    max_value=300,
    value=100,
    step=20,
)


# =========================================================
# Summary
# =========================================================

st.header("Graph Overview")

summary = queries.get_summary()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Entities",
        summary["total_entities"],
    )

with col2:
    st.metric(
        "Relationships",
        summary["total_relationships"],
    )

with col3:
    st.metric(
        "Communities",
        summary["total_communities"],
    )


# =========================================================
# Entity Distribution
# =========================================================

st.header("Entity Distribution")

entity_distribution = queries.get_entity_type_distribution()

if entity_distribution:

    df_entities = pd.DataFrame(entity_distribution)

    if {"type", "total"}.issubset(df_entities.columns):
        st.bar_chart(
            df_entities.set_index("type")["total"]
        )
    else:
        st.warning(
            "Entity distribution is not available in the expected shape."
        )


# =========================================================
# Relationship Distribution
# =========================================================

st.header("Relationship Distribution")

relationship_distribution = (
    queries.get_relationship_distribution()
)

if relationship_distribution:

    df_relationships = pd.DataFrame(
        relationship_distribution
    )

    if {"relationship_type", "total"}.issubset(
        df_relationships.columns
    ):
        st.bar_chart(
            df_relationships.set_index(
                "relationship_type"
            )["total"]
        )

        st.dataframe(
            df_relationships,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning(
            "Relationship distribution is not available in the expected shape."
        )


# =========================================================
# Centrality Analytics
# =========================================================

st.header("Centrality Analytics")

tab1, tab2, tab3 = st.tabs(
    [
        "Degree",
        "Betweenness",
        "Closeness",
    ]
)


# ---------------------------------------------------------
# Degree
# ---------------------------------------------------------

with tab1:

    degree_data = queries.get_top_degree_entities(
        top_n
    )

    if degree_data:

        df = pd.DataFrame(degree_data)

        st.subheader(
            "Top Entities by Degree Centrality"
        )

        st.bar_chart(
            df.set_index("name")["degree"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------
# Betweenness
# ---------------------------------------------------------

with tab2:

    betweenness_data = (
        queries.get_top_betweenness_entities(
            top_n
        )
    )

    if betweenness_data:

        df = pd.DataFrame(
            betweenness_data
        )

        st.subheader(
            "Top Entities by Betweenness Centrality"
        )

        st.bar_chart(
            df.set_index("name")["betweenness"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------
# Closeness
# ---------------------------------------------------------

with tab3:

    closeness_data = (
        queries.get_top_closeness_entities(
            top_n
        )
    )

    if closeness_data:

        df = pd.DataFrame(
            closeness_data
        )

        st.subheader(
            "Top Entities by Closeness Centrality"
        )

        st.bar_chart(
            df.set_index("name")["closeness"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# Risk Analytics
# =========================================================

st.header("Risk Analytics")

risk_distribution = queries.get_risk_distribution()

if risk_distribution:

    df_risk_distribution = pd.DataFrame(
        risk_distribution
    )

    if {"risk_level", "total"}.issubset(
        df_risk_distribution.columns
    ):
        st.bar_chart(
            df_risk_distribution.set_index(
                "risk_level"
            )["total"]
        )
    else:
        st.warning(
            "Risk-level distribution is not available in the expected shape."
        )


st.subheader("Highest Risk Entities")

risk_data = queries.get_top_risk_entities(
    top_n
)

if risk_data:

    df_risk = pd.DataFrame(risk_data)

    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# Community Analytics
# =========================================================

st.header("Community Analytics")

community_data = (
    queries.get_community_summary()
)

if community_data:

    df_communities = pd.DataFrame(
        community_data
    )

    st.dataframe(
        df_communities,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "Community Average Risk"
    )

    st.bar_chart(
        df_communities.set_index(
            "community"
        )["avg_risk"]
    )


# =========================================================
# Community Explorer
# =========================================================

if community_data:

    community_values = [
        row["community"]
        for row in community_data
    ]

    selected_community = st.selectbox(
        "Select Community",
        community_values,
    )

    members = queries.get_community_members(
        selected_community
    )

    if members:

        st.subheader(
            f"Community {selected_community} Members"
        )

        df_members = pd.DataFrame(
            members
        )

        st.dataframe(
            df_members,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# Entity Explorer
# =========================================================

st.header("Entity Explorer")

entity_names = [
    row["name"]
    for row in queries.get_top_risk_entities(100)
]

if entity_names:

    selected_entity = st.selectbox(
        "Select Entity",
        entity_names,
    )

    entity_details = (
        queries.get_entity_details(
            selected_entity
        )
    )

    if entity_details:

        st.json(
            entity_details[0]
        )


# =========================================================
# Graph Data
# =========================================================

st.header("Graph Relationships")

graph_data = queries.get_graph_data(
    graph_limit
)

if graph_data:

    df_graph = pd.DataFrame(
        graph_data
    )

    st.dataframe(
        df_graph,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "Supply Chain Intelligence Platform | "
    "Neo4j + Graph Data Science + Risk Analytics"
)