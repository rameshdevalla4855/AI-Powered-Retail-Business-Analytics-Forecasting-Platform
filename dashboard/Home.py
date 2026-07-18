import importlib.util
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.components.cards import metric_row, module_card
from dashboard.components.sidebar import show_sidebar
from dashboard.utils import load_data
from src.analytics import get_kpis

st.set_page_config(page_title="RetailIQ AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.session_state.setdefault("router_mode", True)
show_sidebar()

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_home_page() -> None:
    df = load_data()
    kpis = get_kpis(df)

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#0f172a 0%,#1d4ed8 50%,#2563eb 100%); padding:26px 28px; border-radius:20px; color:white; box-shadow:0 10px 30px rgba(15,23,42,0.18);">
            <h1 style="margin:0; font-size:2rem;">🛒 RetailIQ AI</h1>
            <p style="margin-top:8px; font-size:1.03rem; line-height:1.6; color:#e2e8f0;">A polished decision intelligence workspace for retail teams to explore revenue, customer behavior, forecasting, recommendations, and AI-driven analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col1, col2 = st.columns([1.4, 0.8], gap="large")
    with col1:
        st.subheader("What this platform delivers")
        st.markdown(
            "- Executive-ready KPI monitoring and sales storytelling\n"
            "- Rich customer segmentation and retention insights\n"
            "- Forecasting and product recommendation workflows\n"
            "- Conversational analytics for business questions"
        )
    with col2:
        st.subheader("Quick snapshot")
        st.markdown(
            "- 100K+ orders\n"
            "- 30K+ products\n"
            "- 3K+ sellers\n"
            "- Delivery, payment, and review enrichment"
        )

    metric_row([
        {"title": "Total Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💰"},
        {"title": "Orders", "value": f"{kpis['Total Orders']:,}", "icon": "🛒"},
        {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👤"},
        {"title": "Products", "value": f"{kpis['Total Products']:,}", "icon": "📦"},
    ])

    st.markdown("---")

    st.subheader("Core modules")
    module_columns = st.columns(2)
    with module_columns[0]:
        module_card("Executive Dashboard", "Track the highest-value KPIs and business performance in one place.", "📊", "pages/1_Executive_Dashboard.py")
        module_card("Customer Segmentation", "Understand customer clusters and profile key audience groups.", "🧠", "pages/4_Customer_Segmentation.py")
    with module_columns[1]:
        module_card("Sales Analytics", "Explore trends, categories, and seller performance with rich visuals.", "📈", "pages/2_Sales_Analytics.py")
        module_card("AI Data Analyst", "Ask questions in plain language and receive business-ready analytics.", "🤖", "pages/7_AI_Data_Analyst.py")

    st.markdown("---")

    st.subheader("Technology stack")
    st.markdown("Python, Streamlit, Plotly, Pandas, Scikit-learn, Joblib, and Pillow")

    st.caption("Developed by Ramesh Devalla | B.Tech Artificial Intelligence & Data Science")


def render_page(page_name: str) -> None:
    page_map = {
        "Home": None,
        "Executive Dashboard": "dashboard/pages/1_Executive_Dashboard.py",
        "Sales Analytics": "dashboard/pages/2_Sales_Analytics.py",
        "Customer Analytics": "dashboard/pages/3_Customer_Analytics.py",
        "Customer Segmentation": "dashboard/pages/4_Customer_Segmentation.py",
        "Sales Forecasting": "dashboard/pages/5_Sales_Forecasting.py",
        "Product Recommendation": "dashboard/pages/6_Product_Recommendation.py",
        "AI Data Analyst": "dashboard/pages/7_AI_Data_Analyst.py",
        "Project Insights": "dashboard/pages/8_Project_Insights.py",
    }

    if page_name == "Home" or page_name not in page_map:
        render_home_page()
        return

    page_path = Path(page_map[page_name])
    spec = importlib.util.spec_from_file_location(page_path.stem, page_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[page_path.stem] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)


selected_page = st.session_state.get("selected_page", "Home")
render_page(selected_page)

