"""Natural language-style analytics assistant for the dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.cards import metric_row
from dashboard.components.charts import bar_chart, line_chart, pie_chart
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_kpi_summary
from src.analytics import monthly_sales, payment_analysis, top_products, top_sellers

st.set_page_config(page_title="AI Data Analyst", page_icon="🤖", layout="wide")
show_sidebar()

st.title("🤖 AI Data Analyst")
st.caption("Ask simple business questions and get charts, KPIs, and tables")

try:
    df = get_dashboard_data()
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load data: {exc}")
    st.stop()

with st.sidebar:
    st.subheader("Query Controls")
    selected_states = st.multiselect("State", sorted(df["customer_state"].dropna().unique().tolist()))
    selected_categories = st.multiselect("Category", sorted(df["product_category_name_english"].dropna().unique().tolist()))

query = st.text_input("Ask a question", value="Show monthly sales")

filtered = df.copy()
if selected_states:
    filtered = filtered[filtered["customer_state"].isin(selected_states)]
if selected_categories:
    filtered = filtered[filtered["product_category_name_english"].isin(selected_categories)]

if filtered.empty:
    st.warning("No rows match the current filters.")
    st.stop()

kpis = get_kpi_summary(filtered)
metric_row([
    {"title": "Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💰"},
    {"title": "Orders", "value": f"{kpis['Total Orders']:,}", "icon": "🛒"},
    {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👥"},
])

st.markdown("---")

text = query.lower()
if "monthly" in text and "sales" in text:
    result = monthly_sales(filtered)
    st.plotly_chart(line_chart(result, "purchase_month", "payment_value", "Monthly Sales"), use_container_width=True)
    show_table(result, "Monthly Sales")
elif "top products" in text:
    result = top_products(filtered, top_n=10)
    st.plotly_chart(bar_chart(result.rename(columns={"payment_value": "Revenue"}), "product_id", "Revenue", "Top Products"), use_container_width=True)
    show_table(result, "Top Products")
elif "revenue by state" in text:
    result = filtered.groupby("customer_state")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    st.plotly_chart(bar_chart(result, "customer_state", "payment_value", "Revenue by State"), use_container_width=True)
    show_table(result, "Revenue by State")
elif "payment" in text:
    result = payment_analysis(filtered)
    st.plotly_chart(pie_chart(result, "payment_type", "Revenue", "Payment Distribution"), use_container_width=True)
    show_table(result, "Payment Analysis")
elif "best customers" in text:
    result = filtered.groupby("customer_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False).head(10)
    st.plotly_chart(bar_chart(result, "customer_id", "payment_value", "Best Customers"), use_container_width=True)
    show_table(result, "Best Customers")
else:
    st.info("Try one of these prompts: 'Show monthly sales', 'Top products', 'Revenue by state', 'Payment distribution', or 'Best customers'.")
