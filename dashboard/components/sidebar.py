"""Reusable sidebar content for the RetailIQ AI dashboard."""

from __future__ import annotations

import streamlit as st


def show_sidebar() -> None:
    """Display the common sidebar across all dashboard pages."""
    with st.sidebar:
        st.markdown("<div style='font-size:2rem; text-align:center;'>🛒</div>", unsafe_allow_html=True)
        st.title("RetailIQ AI")
        st.caption("AI Powered Retail Business Analytics Platform")
        st.divider()

        st.subheader("Core Modules")

        navigation = [
            ("Home", "Home.py"),
            ("📊 Executive Dashboard", "pages/1_Executive_Dashboard.py"),
            ("📈 Sales Analytics", "pages/2_Sales_Analytics.py"),
            ("👥 Customer Analytics", "pages/3_Customer_Analytics.py"),
            ("🧠 Customer Segmentation", "pages/4_Customer_Segmentation.py"),
            ("🔮 Sales Forecasting", "pages/5_Sales_Forecasting.py"),
            ("🛍 Product Recommendation", "pages/6_Product_Recommendation.py"),
            ("🤖 AI Data Analyst", "pages/7_AI_Data_Analyst.py"),
            ("💡 Project Insights", "pages/8_Project_Insights.py"),
        ]

        for label, page_name in navigation:
            st.page_link(page_name, label=label)

        st.divider()
        st.subheader("Dataset Snapshot")
        st.info("""**Olist E-Commerce Dataset**\n\n- 100K+ Orders\n- 30K+ Products\n- 3K+ Sellers""")

        st.divider()
        st.caption("Developed by Ramesh Devalla")
        st.caption("B.Tech Artificial Intelligence & Data Science")