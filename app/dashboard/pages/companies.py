"""
Companies Page - Company Search and Supply Chain Analysis

Displays company information, supplier relationships, and dependency metrics.
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
    st.title("🏢 Companies")
    st.markdown(
        """Welcome to the companies directory. Search for companies, view their
        supplier relationships, and analyze dependency metrics."""
    )
    st.divider()


def render_company_search(queries: DashboardQueries) -> str | None:
    """Render company search input and return selected company name."""
    st.subheader("🔍 Search Company")
    col1, col2 = st.columns([4, 1])
    with col1:
        company_name = st.text_input(
            "Enter company name:",
            placeholder="e.g., Apple, NVIDIA, AMD",
            help="Type a company name to look up its supply-chain data.",
        )
    with col2:
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if search_btn and company_name:
        with st.spinner(f"Loading data for {company_name}..."):
            entity_details = queries.get_entity_details(company_name)
            if not entity_details or entity_details[0].get("name") != company_name:
                st.warning(
                    f"Company '{company_name}' not found in the knowledge graph. "
                    "Please check the spelling or try another company."
                )
                return None
        return company_name




def render_company_details(company_name: str, queries: DashboardQueries) -> None:
    """Render detailed company information and dependency metrics."""
    st.subheader(f"Company: {company_name}")

    entity_details = queries.get_entity_details(company_name)
    if not entity_details:
        st.error(f"Unable to fetch details for {company_name}.")
        return

    entity = entity_details[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Entity Type",
            entity.get("type", "N/A"),
            help="Type of entity in the knowledge graph",
        )
    with col2:
        st.metric(
            "Degree",
            entity.get("degree", 0),
            help="Number of connections/relationships",
        )
    with col3:
        st.metric(
            "Supplier Dependency",
            f"{entity.get('supplier_dependency', 0):.4f}",
            help="Proportion of suppliers (0-1)",
        )
    with col4:
        st.metric(
            "Country Dependency",
            f"{entity.get('country_dependency', 0):.4f}",
            help="Proportion of country dependencies (0-1)",
        )

    st.divider()

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**Tier-1 Dependencies**")
        tier1 = entity.get("tier1_dependency", 0)
        st.caption(f"Score: {tier1:.4f}")

    with col6:
        st.markdown("**Tier-2 Dependencies**")
        tier2 = entity.get("tier2_dependency", 0)
        st.caption(f"Score: {tier2:.4f}")

    st.divider()

    col7, col8 = st.columns(2)
    with col7:
        risk_score = entity.get("risk_score", 0)
        st.metric("Risk Score", f"{risk_score:.2f}")
    with col8:
        risk_level = entity.get("risk_level", "N/A")
        st.metric("Risk Level", risk_level)

    st.divider()

    st.markdown("**Suppliers**")
    try:
        suppliers = queries.get_suppliers(company_name, limit=20)
        if suppliers:
            df_suppliers = pd.DataFrame(suppliers)
            if {"supplier", "supplier_type", "total_occurrence_count"}.issubset(
                df_suppliers.columns
            ):
                st.dataframe(
                    df_suppliers.rename(
                        columns={
                            "supplier": "Supplier",
                            "supplier_type": "Type",
                            "total_occurrence_count": "Occurrences",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.dataframe(df_suppliers, use_container_width=True, hide_index=True)
        else:
            st.info(f"No suppliers found for {company_name}.")
    except Exception as e:
        logger.warning(f"Unable to load suppliers for {company_name}: {e}")
        st.warning(f"Unable to load suppliers: {e}")

    st.divider()

    st.markdown("**Compare with Another Company**")
    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        compare_company_1 = st.text_input(
            "Company 1:", placeholder="e.g., Apple", key="compare1"
        )
    with col_comp2:
        compare_company_2 = st.text_input(
            "Company 2:", placeholder="e.g., NVIDIA", key="compare2"
        )

    if compare_company_1 and compare_company_2:
        if st.button("Find Common Suppliers", type="secondary"):
            with st.spinner("Finding common suppliers..."):
                common = queries.get_common_suppliers(
                    compare_company_1, compare_company_2, limit=10
                )
                if common:
                    supplier_names = [s["supplier"] for s in common]
                    st.success(
                        f"Common suppliers between {compare_company_1} and "
                        f"{compare_company_2}: {', '.join(supplier_names)}"
                    )
                    df_common = pd.DataFrame(common)
                    st.dataframe(
                        df_common.rename(
                            columns={
                                "supplier": "Supplier",
                                "total_occurrence_count": "Strength",
                            }
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info(
                        f"No common suppliers found between "
                        f"{compare_company_1} and {compare_company_2}."
                    )


def main() -> None:
    """Render the Companies page."""
    try:
        queries = get_queries()
        render_header()
        company_name = render_company_search(queries)
        if company_name:
            render_company_details(company_name, queries)
    except Exception as e:
        logger.error(f"Error rendering companies page: {e}")
        st.error("An error occurred while rendering the companies page.")


if __name__ == "__main__":
    main()
