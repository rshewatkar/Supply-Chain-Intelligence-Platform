"""
Supply Chain Intelligence Platform — Dashboard Entry Point.

Streamlit's multipage convention automatically discovers files
inside app/dashboard/pages/. This file is the single entry point
that configures the app and provides sidebar navigation.

Run with:
    streamlit run app/dashboard/app.py

Or via script:
    python -m scripts.run_dashboard
"""

import streamlit as st


def main() -> None:
    """Run the Supply Chain Intelligence Platform dashboard."""

    st.set_page_config(
        page_title="Supply Chain Intelligence Platform",
        page_icon="🔗",
        layout="wide",
    )

    # =========================================================
    # Sidebar Navigation
    # =========================================================

    page_names = [
        "Home",
        "Companies",
        "Graph",
        "Risk",
        "Analytics",
        "AI Assistant",
    ]

    page_modules = {
        "Home": "app.dashboard.pages.home",
        "Companies": "app.dashboard.pages.companies",
        "Graph": "app.dashboard.pages.graph",
        "Risk": "app.dashboard.pages.risk",
        "Analytics": "app.dashboard.pages.analytics",
        "AI Assistant": "app.dashboard.pages.ai_assistant",
    }

    selected_page = st.sidebar.radio(
        "Navigation",
        options=page_names,
        index=0,
    )

    # =========================================================
    # Page Content
    # =========================================================

    st.title(selected_page)
    st.markdown(
        """
        Explore supply-chain networks, company dependencies,
        risk indicators, graph analytics, and AI-powered insights.
        """
    )
    st.divider()

    # Dynamically import and run the selected page
    import importlib

    module_path = page_modules[selected_page]
    module = importlib.import_module(module_path)
    module.main()


if __name__ == "__main__":
    main()