"""
Risk Analytics Page - Real-time Risk Monitoring and Intelligence

Displays risk distributions, top risky entities, dependency vulnerabilities,
and centrality risk metrics.
All data is fetched live from Neo4j using RiskDashboardBackend.
"""

import streamlit as st
import pandas as pd

from app.dashboard.risk_dashboard_backend import RiskDashboardBackend
from app.utils.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def get_backend() -> RiskDashboardBackend:
    """Get cached RiskDashboardBackend instance."""
    return RiskDashboardBackend()


# =========================================================
# Sidebar Controls
# =========================================================

def render_sidebar_controls() -> int:
    """Render sidebar controls and return limit parameter."""
    st.sidebar.header("⚠️ Risk Controls")
    
    limit: int = st.sidebar.slider(
        "Entities to display",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
        help="Maximum number of entities shown in risk tables.",
    )
    
    return limit


# =========================================================
# Header
# =========================================================

def render_header() -> None:
    """Render page header and introduction."""
    st.title("⚠️ Risk Analytics")
    st.markdown(
        "Monitor supply chain vulnerabilities, dependency risks, "
        "and overall entity risk profiles across the knowledge graph."
    )
    st.divider()


# =========================================================
# Risk Overview Metrics
# =========================================================

def render_overview_metrics(backend: RiskDashboardBackend) -> None:
    """Render high-level risk statistics in top columns."""
    try:
        overview = backend.get_risk_overview()
        if not overview:
            st.info("No risk overview data available.")
            return
            
        st.subheader("📊 Risk Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total Entities",
                f"{overview.get('total_entities', 0):,}",
            )
        with col2:
            st.metric(
                "Avg Risk Score",
                f"{overview.get('average_risk_score', 0):.1f}",
            )
        with col3:
            st.metric(
                "Max Risk Score",
                f"{overview.get('maximum_risk_score', 0):.1f}",
            )
        with col4:
            st.metric(
                "Critical Risk",
                f"{overview.get('critical_entities', 0):,}",
            )
        with col5:
            st.metric(
                "High Risk",
                f"{overview.get('high_entities', 0):,}",
            )
            
    except Exception as e:
        logger.error(f"Error rendering risk overview: {e}")
        st.error("Unable to load risk overview metrics.")


# =========================================================
# Risk Distributions
# =========================================================

def render_risk_distributions(backend: RiskDashboardBackend) -> None:
    """Render distributions of risk across levels and entity types in columns."""
    try:
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Risk Level Distribution")
            dist_data = backend.get_risk_distribution()
            if dist_data:
                df_dist = pd.DataFrame(dist_data)
                
                # Setup ordering for risk levels if present
                risk_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]
                df_dist['risk_level'] = pd.Categorical(df_dist['risk_level'], categories=risk_order, ordered=True)
                df_dist = df_dist.sort_values('risk_level')
                
                st.bar_chart(df_dist.set_index("risk_level")["total"], use_container_width=True)
            else:
                st.info("No risk distribution data.")
                
        with col2:
            st.subheader("🏢 Risk by Entity Type")
            type_data = backend.get_risk_by_entity_type()
            if type_data:
                df_type = pd.DataFrame(type_data)
                st.bar_chart(df_type.set_index("type")["avg_risk"], use_container_width=True)
            else:
                st.info("No entity type risk data.")
                
    except Exception as e:
        logger.error(f"Error rendering risk distributions: {e}")
        st.warning("Unable to load risk distributions.")


# =========================================================
# Detailed Risk Tables (Tabs)
# =========================================================

def render_detailed_risk_tabs(backend: RiskDashboardBackend, limit: int) -> None:
    """Render detailed data tables segregated into tabs."""
    try:
        st.divider()
        st.subheader("📋 Comprehensive Risk Analysis")
        
        tab1, tab2, tab3 = st.tabs([
            "🚨 Highest Risk Entities",
            "🔗 Dependency Risks",
            "🕸️ Centrality Risks"
        ])
        
        with tab1:
            _render_highest_risk_table(backend, limit)
            
        with tab2:
            _render_dependency_risk_table(backend, limit)
            
        with tab3:
            _render_centrality_risk_table(backend, limit)
            
    except Exception as e:
        logger.error(f"Error rendering detailed risk tabs: {e}")
        st.error("Unable to load detailed risk analysis tables.")


def _render_highest_risk_table(backend: RiskDashboardBackend, limit: int) -> None:
    entities = backend.get_top_risky_entities(limit=limit)
    if not entities:
        st.info("No high-risk entities found.")
        return
        
    df = pd.DataFrame(entities)
    # Reorder columns slightly for better top-level view
    cols = ["entity", "type", "risk_score", "risk_level", "supplier_dependency", "country_dependency", "tier1_dependency", "degree"]
    available_cols = [c for c in cols if c in df.columns]
    
    st.dataframe(
        df[available_cols].rename(columns={
            "entity": "Entity", "type": "Type", "risk_score": "Risk Score", "risk_level": "Risk Level",
            "supplier_dependency": "Supplier Dep.", "country_dependency": "Country Dep.",
            "tier1_dependency": "Tier 1 Dep.", "degree": "Degree (Connections)"
        }),
        use_container_width=True, hide_index=True
    )

def _render_dependency_risk_table(backend: RiskDashboardBackend, limit: int) -> None:
    entities = backend.get_dependency_risk(limit=limit)
    if not entities:
        st.info("No dependency risk data found.")
        return
        
    df = pd.DataFrame(entities)
    st.dataframe(
        df.rename(columns={
            "entity": "Entity", "type": "Type", "risk_score": "Risk Score", "risk_level": "Risk Level",
            "supplier_dependency": "Supplier Dep.", "country_dependency": "Country Dep.",
            "tier1_dependency": "Tier 1 Dep.", "tier2_dependency": "Tier 2 Dep."
        }),
        use_container_width=True, hide_index=True
    )

def _render_centrality_risk_table(backend: RiskDashboardBackend, limit: int) -> None:
    entities = backend.get_centrality_risk(limit=limit)
    if not entities:
        st.info("No centrality risk data found.")
        return
        
    df = pd.DataFrame(entities)
    st.dataframe(
        df.rename(columns={
            "entity": "Entity", "type": "Type", "risk_score": "Risk Score", "risk_level": "Risk Level",
            "degree": "Degree Centrality", "betweenness": "Betweenness", "closeness": "Closeness"
        }),
        use_container_width=True, hide_index=True
    )


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
    """Render the Risk Analytics page."""
    try:
        backend = get_backend()
        
        limit = render_sidebar_controls()
        
        render_header()
        render_overview_metrics(backend)
        render_risk_distributions(backend)
        render_detailed_risk_tabs(backend, limit)
        
        render_footer()
        
    except Exception as e:
        logger.error(f"Error rendering risk page: {e}")
        st.error("An error occurred while rendering the risk analytics page.")


if __name__ == "__main__":
    main()
