"""Reusable sidebar content for the RetailIQ AI dashboard."""

from __future__ import annotations

import streamlit as st


def show_sidebar() -> None:
    """Display the common sidebar across all dashboard pages."""
    if "sidebar_css" not in st.session_state:
        st.markdown(
            """
            <style>
            div[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
            }
            div[data-testid="stSidebarNav"] a {
                border-radius: 10px;
                padding: 0.45rem 0.6rem;
                margin: 0.15rem 0;
                color: #0f172a;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["sidebar_css"] = True

    with st.sidebar:
        st.markdown("<div style='font-size:2rem; text-align:center;'>🛒</div>", unsafe_allow_html=True)
        st.title("RetailIQ AI")
        st.caption("AI Powered Retail Business Analytics Platform")
        st.divider()

        st.subheader("Navigate")
        options = [
            "Home",
            "Executive Dashboard",
            "Sales Analytics",
            "Customer Analytics",
            "Customer Segmentation",
            "Sales Forecasting",
            "Product Recommendation",
            "AI Data Analyst",
            "Project Insights",
        ]
        current_selection = st.session_state.get("selected_page", "Home")
        if current_selection not in options:
            current_selection = "Home"

        selected_page = st.radio(
            "Go to",
            options,
            key="selected_page_widget",
            index=options.index(current_selection),
        )
        st.session_state["selected_page"] = selected_page

        st.divider()
        st.subheader("Dataset Snapshot")
        st.info("""**Olist E-Commerce Dataset**\n\n- 100K+ Orders\n- 30K+ Products\n- 3K+ Sellers""")

        st.divider()
        st.caption("Developed by Ramesh Devalla")
        st.caption("B.Tech Artificial Intelligence & Data Science")