import streamlit as st


st.title("Home")

st.markdown(
    """
    ## Supply Chain Intelligence Platform

    Monitor companies, supply-chain relationships, dependency,
    risk, graph analytics, and AI-powered supply-chain insights.
    """
)

st.divider()

st.subheader("Platform Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Companies", "10")

with col2:
    st.metric("Knowledge Graph", "Active")

with col3:
    st.metric("AI Assistant", "Available")