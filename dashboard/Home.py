import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.components.cards import metric_row
from dashboard.components.sidebar import show_sidebar
from dashboard.utils import load_data
from src.analytics import get_kpis

st.set_page_config(page_title="RetailIQ AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
show_sidebar()

df = load_data()
kpis = get_kpis(df)

st.markdown(
    """
    <div style="background:linear-gradient(135deg,#0f172a,#1d4ed8);padding:24px;border-radius:18px;color:white;">
        <h1 style="margin:0;">🛒 RetailIQ AI</h1>
        <p style="margin-top:8px; font-size:1.05rem;">AI-powered retail business analytics platform for executives, analysts, and data science teams.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.subheader("Project Description")
st.markdown(
    "RetailIQ AI transforms the Olist e-commerce dataset into an interactive decision intelligence experience with forecasting, segmentation, recommendations, and conversational analytics."
)

metric_row([
    {"title": "Total Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💰"},
    {"title": "Orders", "value": f"{kpis['Total Orders']:,}", "icon": "🛒"},
    {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👤"},
    {"title": "Products", "value": f"{kpis['Total Products']:,}", "icon": "📦"},
])

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Business Overview")
    st.markdown("- Executive-ready KPIs and sales performance analysis\n- Customer segmentation and retention intelligence\n- Forecasting and recommendation modules\n- Natural language analytics for business questions")
with col2:
    st.subheader("Dataset Snapshot")
    st.markdown("- 100K+ orders\n- 30K+ products\n- 3K+ sellers\n- enriched delivery, review, and payment features")

st.markdown("---")

st.subheader("Core Modules")
mod_cols = st.columns(4)
with mod_cols[0]:
    st.info("📊 Executive Dashboard")
with mod_cols[1]:
    st.info("📈 Sales Analytics")
with mod_cols[2]:
    st.info("🧠 Customer Segmentation")
with mod_cols[3]:
    st.info("🤖 AI Data Analyst")

st.markdown("---")

st.subheader("Technology Stack")
st.markdown("Python, Streamlit, Plotly, Pandas, Scikit-learn, Joblib, Pillow")

st.subheader("Machine Learning Models")
st.markdown("- Sales forecasting with regression models\n- Customer segmentation with KMeans\n- Product recommendations with cosine similarity")

st.markdown("---")
st.caption("Developed by Ramesh Devalla | B.Tech Artificial Intelligence & Data Science")
