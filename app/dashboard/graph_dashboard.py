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
    ### Graph Analytics & Risk Dashboard

    Explore supply-chain entities, relationships,
    graph centrality, communities, dependency metrics,
    and risk analytics.
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
# Graph Overview
# =========================================================

st.header("Graph Overview")

summary = queries.get_summary()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Entities",
        summary.get("total_entities", 0),
    )

with col2:
    st.metric(
        "Relationships",
        summary.get("total_relationships", 0),
    )

with col3:
    st.metric(
        "Communities",
        summary.get("total_communities", 0),
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

        st.dataframe(
            df_entities,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.warning(
            "Entity distribution is not available "
            "in the expected format."
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
            "Relationship distribution is not available "
            "in the expected format."
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

        if {"name", "degree"}.issubset(df.columns):

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

        if {"name", "betweenness"}.issubset(
            df.columns
        ):

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

        if {"name", "closeness"}.issubset(
            df.columns
        ):

            st.bar_chart(
                df.set_index("name")["closeness"]
            )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# RISK DASHBOARD
# =========================================================

st.header("Risk Dashboard")

st.markdown(
    """
    Risk metrics are read from the values calculated and
    persisted by the Risk Score Engine.
    """
)


# =========================================================
# Risk Level Summary
# =========================================================

st.subheader("Risk Level Distribution")

risk_distribution = (
    queries.get_risk_distribution()
)

if risk_distribution:

    df_risk_distribution = pd.DataFrame(
        risk_distribution
    )

    if {"risk_level", "total"}.issubset(
        df_risk_distribution.columns
    ):

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(
                df_risk_distribution.set_index(
                    "risk_level"
                )["total"]
            )

        with col2:
            st.dataframe(
                df_risk_distribution,
                use_container_width=True,
                hide_index=True,
            )

    else:
        st.warning(
            "Risk distribution is not available "
            "in the expected format."
        )


# =========================================================
# Highest Risk Entities
# =========================================================

st.subheader("Highest Risk Entities")

risk_data = queries.get_top_risk_entities(
    top_n
)

if risk_data:

    df_risk = pd.DataFrame(
        risk_data
    )

    if "risk_score" in df_risk.columns:

        st.dataframe(
            df_risk,
            use_container_width=True,
            hide_index=True,
        )

else:

    st.info(
        "No risk-scored entities were found."
    )


# =========================================================
# Risk Score Chart
# =========================================================

if risk_data:

    df_risk_chart = pd.DataFrame(
        risk_data
    )

    if {"name", "risk_score"}.issubset(
        df_risk_chart.columns
    ):

        st.subheader(
            "Risk Score by Entity"
        )

        st.bar_chart(
            df_risk_chart.set_index(
                "name"
            )["risk_score"]
        )


# =========================================================
# Dependency Risk Metrics
# =========================================================

st.subheader("Dependency Risk Metrics")

if risk_data:

    df_dependency = pd.DataFrame(
        risk_data
    )

    dependency_columns = [
        "name",
        "supplier_dependency",
        "country_dependency",
        "tier1_dependency",
        "tier2_dependency",
        "risk_score",
        "risk_level",
    ]

    available_columns = [
        column
        for column in dependency_columns
        if column in df_dependency.columns
    ]

    if available_columns:

        st.dataframe(
            df_dependency[available_columns],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Dependency metrics are not available "
            "from DashboardQueries."
        )


# =========================================================
# Risk Entity Explorer
# =========================================================

st.subheader("Risk Entity Explorer")

risk_entities = queries.get_top_risk_entities(
    100
)

if risk_entities:

    risk_entity_names = [
        row["name"]
        for row in risk_entities
        if row.get("name")
    ]

    if risk_entity_names:

        selected_risk_entity = st.selectbox(
            "Select entity for risk analysis",
            risk_entity_names,
            key="risk_entity_selector",
        )

        selected_entity_data = [
            row
            for row in risk_entities
            if row.get("name")
            == selected_risk_entity
        ]

        if selected_entity_data:

            entity = selected_entity_data[0]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Risk Score",
                    f"{entity.get('risk_score', 0):.4f}",
                )

            with col2:
                st.metric(
                    "Risk Level",
                    entity.get(
                        "risk_level",
                        "UNKNOWN",
                    ),
                )

            with col3:
                st.metric(
                    "Supplier Dependency",
                    f"{entity.get('supplier_dependency', 0):.4f}",
                )

            st.write("### Dependency Breakdown")

            dependency_data = {
                "Metric": [
                    "Supplier Dependency",
                    "Country Dependency",
                    "Tier-1 Dependency",
                    "Tier-2 Dependency",
                    "Risk Score",
                ],
                "Value": [
                    entity.get(
                        "supplier_dependency",
                        0,
                    ),
                    entity.get(
                        "country_dependency",
                        0,
                    ),
                    entity.get(
                        "tier1_dependency",
                        0,
                    ),
                    entity.get(
                        "tier2_dependency",
                        0,
                    ),
                    entity.get(
                        "risk_score",
                        0,
                    ),
                ],
            }

            df_selected_risk = pd.DataFrame(
                dependency_data
            )

            st.dataframe(
                df_selected_risk,
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

    if {
        "community",
        "avg_risk",
    }.issubset(df_communities.columns):

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
        if row.get("community") is not None
    ]

    if community_values:

        selected_community = st.selectbox(
            "Select Community",
            community_values,
            key="community_selector",
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
    if row.get("name")
]

if entity_names:

    selected_entity = st.selectbox(
        "Select Entity",
        entity_names,
        key="entity_selector",
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
# Graph Relationships
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