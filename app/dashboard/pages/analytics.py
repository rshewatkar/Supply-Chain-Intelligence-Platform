"""
Analytics Page - Supply Chain Analytics & Risk Intelligence.

Displays comprehensive supply chain analytics including risk scoring,
community analysis, tier dependencies, and country/supplier dependency
metrics. All data is fetched live from Neo4j using analytics engines.
"""

import streamlit as st
import pandas as pd
from app.analytics.risk_score_engine import RiskScoreEngine
from app.analytics.community_report import CommunityReport
from app.analytics.tier_analysis import TierAnalysis
from app.analytics.country_dependency import CountryDependency
from app.analytics.supplier_dependency import SupplierDependency
from app.utils.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def get_risk_engine() -> RiskScoreEngine:
    """Get cached RiskScoreEngine instance."""
    return RiskScoreEngine()


@st.cache_resource
def get_community_report() -> CommunityReport:
    """Get cached CommunityReport instance."""
    return CommunityReport()


@st.cache_resource
def get_tier_analysis() -> TierAnalysis:
    """Get cached TierAnalysis instance."""
    return TierAnalysis()


@st.cache_resource
def get_country_dependency() -> CountryDependency:
    """Get cached CountryDependency instance."""
    return CountryDependency()


@st.cache_resource
def get_supplier_dependency() -> SupplierDependency:
    """Get cached SupplierDependency instance."""
    return SupplierDependency()


# =========================================================
# Sidebar Controls
# =========================================================


def render_sidebar_controls() -> dict:
    """Render sidebar controls and return user-selected parameters."""
    st.sidebar.header("📊 Analytics Controls")

    top_n: int = st.sidebar.slider(
        "Entities to display",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
        help="Controls how many entities appear in top lists.",
    )

    return {"top_n": top_n}
# =========================================================
# Header
# =========================================================


def render_header() -> None:
    """Render page header and introduction."""
    st.title("📈 Analytics")
    st.markdown(
        "Comprehensive supply chain analytics including risk scoring, "
        "community analysis, tier dependencies, and country/supplier "
        "dependency metrics."
    )
    st.divider()


# =========================================================
# Risk Analytics Section
# =========================================================


def render_risk_analytics(engine: RiskScoreEngine, limit: int) -> None:
    """Render comprehensive risk analytics section."""
    st.subheader("⚠️ Risk Analytics")

    try:
        st.markdown("**🔥 Top Risky Entities**")
        top_entities = engine.top_risky_entities(limit=limit)
        if top_entities:
            df_entities = pd.DataFrame(top_entities)
            cols = [
                "name",
                "entity_type",
                "risk_score",
                "risk_level",
                "supplier_dependency",
                "country_dependency",
                "tier1_dependency",
                "tier2_dependency",
                "degree",
                "betweenness",
                "closeness",
            ]
            available_cols = [c for c in cols if c in df_entities.columns]
            st.dataframe(
                df_entities[available_cols].rename(
                    columns={
                        "name": "Entity",
                        "entity_type": "Type",
                        "risk_score": "Risk Score",
                        "risk_level": "Risk Level",
                        "supplier_dependency": "Supplier Dep.",
                        "country_dependency": "Country Dep.",
                        "tier1_dependency": "Tier 1 Dep.",
                        "tier2_dependency": "Tier 2 Dep.",
                        "degree": "Degree",
                        "betweenness": "Betweenness",
                        "closeness": "Closeness",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No risk data available yet.")
    except Exception as e:
        logger.error(f"Error rendering risk analytics: {e}")
        st.warning("Unable to load risk analytics data.")
# =========================================================
# Community Analytics Section
# =========================================================


def render_community_analytics(report: CommunityReport, limit: int) -> None:
    """Render comprehensive community analytics section."""
    st.subheader("🏘️ Community Analytics")

    try:
        # Community Summary
        st.markdown("**📊 Community Summary**")
        summary = report.community_summary()
        if summary:
            df_summary = pd.DataFrame(summary)
            cols = ["community", "node_count", "average_risk", "maximum_risk"]
            available_cols = [c for c in cols if c in df_summary.columns]
            st.dataframe(
                df_summary[available_cols].rename(
                    columns={
                        "community": "Community",
                        "node_count": "Node Count",
                        "average_risk": "Avg Risk",
                        "maximum_risk": "Max Risk",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No community data available yet.")

        # Top Communities
        st.markdown("**🌟 Top Communities**")
        top_communities = report.top_communities(limit=limit)
        if top_communities:
            df_communities = pd.DataFrame(top_communities)
            cols = ["community", "node_count", "average_degree", "average_risk"]
            available_cols = [c for c in cols if c in df_communities.columns]
            st.dataframe(
                df_communities[available_cols].rename(
                    columns={
                        "community": "Community",
                        "node_count": "Node Count",
                        "average_degree": "Avg Degree",
                        "average_risk": "Avg Risk",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No community data available yet.")

        # Community Risk
        st.markdown("**⚠️ Community Risk**")
        community_risk = report.community_risk()
        if community_risk:
            df_risk = pd.DataFrame(community_risk)
            cols = ["community", "node_count", "average_risk", "maximum_risk", "critical_nodes", "high_risk_nodes"]
            available_cols = [c for c in cols if c in df_risk.columns]
            st.dataframe(
                df_risk[available_cols].rename(
                    columns={
                        "community": "Community",
                        "node_count": "Node Count",
                        "average_risk": "Avg Risk",
                        "maximum_risk": "Max Risk",
                        "critical_nodes": "Critical",
                        "high_risk_nodes": "High Risk",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No community risk data available yet.")

    except Exception as e:
        logger.error(f"Error rendering community analytics: {e}")
        st.warning("Unable to load community analytics data.")
# =========================================================
# Tier Analysis Section
# =========================================================


def render_tier_analysis(analysis: TierAnalysis) -> None:
    """Render comprehensive tier analysis section."""
    st.subheader("🏗️ Tier Analysis")

    try:
        st.markdown("**📊 Tier Dependency Summary**")
        summary = analysis.dependency_summary()
        if summary:
            df_summary = pd.DataFrame(summary)
            cols = ["company", "tier_1_dependencies", "tier_2_dependencies", "tier1_dependency", "tier2_dependency"]
            available_cols = [c for c in cols if c in df_summary.columns]
            st.dataframe(
                df_summary[available_cols].rename(
                    columns={
                        "company": "Company",
                        "tier_1_dependencies": "Tier 1 Count",
                        "tier_2_dependencies": "Tier 2 Count",
                        "tier1_dependency": "Tier 1 Score",
                        "tier2_dependency": "Tier 2 Score",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No tier analysis data available yet.")

    except Exception as e:
        logger.error(f"Error rendering tier analysis: {e}")
        st.warning("Unable to load tier analysis data.")
# =========================================================
# Country Dependency Section
# =========================================================


def render_country_dependency(dep: CountryDependency, limit: int) -> None:
    """Render comprehensive country dependency section."""
    st.subheader("🌍 Country Dependency")

    try:
        st.markdown("**🌐 Top Dependency Countries**")
        top_countries = dep.top_dependency_countries(limit=limit)
        if top_countries:
            df_countries = pd.DataFrame(top_countries)
            cols = ["country", "country_dependency", "degree", "betweenness", "closeness", "risk_score", "risk_level"]
            available_cols = [c for c in cols if c in df_countries.columns]
            st.dataframe(
                df_countries[available_cols].rename(
                    columns={
                        "country": "Country",
                        "country_dependency": "Dependency",
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
            st.info("No country dependency data available yet.")

        st.markdown("**⚠️ Country Dependency Risk**")
        risk_data = dep.country_dependency_risk(limit=limit)
        if risk_data:
            df_risk = pd.DataFrame(risk_data)
            cols = ["country", "connected_entities", "total_relationships", "risk_level"]
            available_cols = [c for c in cols if c in df_risk.columns]
            st.dataframe(
                df_risk[available_cols].rename(
                    columns={
                        "country": "Country",
                        "connected_entities": "Connected Entities",
                        "total_relationships": "Total Relationships",
                        "risk_level": "Risk Level",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No country dependency risk data available yet.")

    except Exception as e:
        logger.error(f"Error rendering country dependency: {e}")
        st.warning("Unable to load country dependency data.")
# =========================================================
# Supplier Dependency Section
# =========================================================


def render_supplier_dependency(dep: SupplierDependency, limit: int) -> None:
    """Render comprehensive supplier dependency section."""
    st.subheader("📦 Supplier Dependency")

    try:
        st.markdown("**🔗 Top Supplier-Dependent Entities**")
        top_entities = dep.top_supplier_dependent_entities(limit=limit)
        if top_entities:
            df_entities = pd.DataFrame(top_entities)
            cols = ["name", "type", "supplier_dependency", "degree", "risk_score", "risk_level"]
            available_cols = [c for c in cols if c in df_entities.columns]
            st.dataframe(
                df_entities[available_cols].rename(
                    columns={
                        "name": "Entity",
                        "type": "Type",
                        "supplier_dependency": "Supplier Dependency",
                        "degree": "Degree",
                        "risk_score": "Risk Score",
                        "risk_level": "Risk Level",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No supplier dependency data available yet.")

        st.markdown("**📊 Supplier Dependency Summary**")
        summary = dep.dependency_summary()
        if summary:
            st.write(f"Total Entities: {summary.get('total_entities', 0)}")
            st.write(f"Very High Dependency (≥75%): {summary.get('very_high_dependency', 0)}")
            st.write(f"High Dependency (50-75%): {summary.get('high_dependency', 0)}")
            st.write(f"Medium Dependency (25-50%): {summary.get('medium_dependency', 0)}")
            st.write(f"Low Dependency (<25%): {summary.get('low_dependency', 0)}")
        else:
            st.info("No supplier dependency summary available yet.")

    except Exception as e:
        logger.error(f"Error rendering supplier dependency: {e}")
        st.warning("Unable to load supplier dependency data.")
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
    """Render the Analytics page."""
    try:
        risk_engine = get_risk_engine()
        community_report = get_community_report()
        tier_analysis = get_tier_analysis()
        country_dep = get_country_dependency()
        supplier_dep = get_supplier_dependency()
        
        controls = render_sidebar_controls()
        top_n: int = controls["top_n"]
        
        render_header()
        render_risk_analytics(risk_engine, top_n)
        render_community_analytics(community_report, top_n)
        render_tier_analysis(tier_analysis)
        render_country_dependency(country_dep, top_n)
        render_supplier_dependency(supplier_dep, top_n)
        
        render_footer()
        
    except Exception as e:
        logger.error(f"Error rendering analytics page: {e}")
        st.error("An error occurred while rendering the analytics page.")


if __name__ == "__main__":
    main()