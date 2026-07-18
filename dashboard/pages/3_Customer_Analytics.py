"""Customer analytics page for the RetailIQ AI dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.cards import metric_row
from dashboard.components.charts import bar_chart, pie_chart, scatter_chart
from dashboard.components.filters import dashboard_filters
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_kpi_summary

show_sidebar()

st.title("👥 Customer Analytics")
st.caption("RFM-style insights, retention signals, and customer geography")

try:
    df = get_dashboard_data()
    filters = dashboard_filters(df)
    filtered = apply_filters(
        df,
        date_range=filters["date_range"],
        states=filters["states"],
        categories=filters["categories"],
        sellers=filters["sellers"],
        payment_types=filters["payment_types"],
    )
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load data: {exc}")
    st.stop()

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

kpis = get_kpi_summary(filtered)
metric_row([
    {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👤"},
    {"title": "Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💳"},
    {"title": "Average Order Value", "value": f"${kpis['Average Order Value']:,.2f}", "icon": "🧾"},
    {"title": "Average Review Score", "value": f"{kpis['Average Review Score']:.1f}", "icon": "⭐"},
])

st.markdown("---")

customer_summary = (
    filtered.groupby("customer_id")
    .agg(
        Orders=("order_id", "nunique"),
        Revenue=("payment_value", "sum"),
        AvgReview=("review_score", "mean"),
        AvgBasket=("payment_value", "mean"),
    )
    .reset_index()
)

customer_summary["AvgBasket"] = customer_summary["AvgBasket"].round(2)
customer_summary = customer_summary.sort_values("Revenue", ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(customer_summary.head(10), "customer_id", "Revenue", "Top Customers by Revenue"), use_container_width=True)
with col2:
    state_summary = (
        filtered.groupby("customer_state")
        .agg(Revenue=("payment_value", "sum"), Customers=("customer_id", "nunique"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    st.plotly_chart(bar_chart(state_summary.head(10), "customer_state", "Revenue", "Revenue by State"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(pie_chart(customer_summary.head(10), "customer_id", "Revenue", "Revenue Share by Top Customers"), use_container_width=True)
with col2:
    st.plotly_chart(scatter_chart(customer_summary, "Orders", "Revenue", "customer_id", "Orders vs Revenue"), use_container_width=True)

st.markdown("---")
show_table(customer_summary.head(20), "Customer Summary")
