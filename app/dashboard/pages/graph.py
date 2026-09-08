import streamlit as st
import pandas as pd
from app.dashboard.dashboard_queries import DashboardQueries

@st.cache_resource
def get_queries():
    return DashboardQueries()

def main() -> None:
    """Graph Analysis page."""
    queries = get_queries()
    
    st.subheader("Graph Analytics")
    
    # You can now easily bring in logic from the old graph_dashboard.py
    summary = queries.get_summary()
    st.metric("Entities", summary.get("total_entities", 0))

    st.write("Full module implementation ongoing...")