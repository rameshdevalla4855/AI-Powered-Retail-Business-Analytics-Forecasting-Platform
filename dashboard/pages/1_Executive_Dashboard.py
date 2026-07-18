"""Executive dashboard page for the RetailIQ AI platform."""

from __future__ import annotations

import streamlit as st

from dashboard.components.cards import metric_row
from dashboard.components.charts import bar_chart, line_chart
from dashboard.components.filters import dashboard_filters
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_kpi_summary
from src.analytics import (
    customer_state_sales,
    monthly_orders,
    monthly_sales,
    payment_analysis,
    review_analysis,
    revenue_by_category,
    top_products,
    top_sellers,
)

show_sidebar()

st.title("📊 Executive Dashboard")
st.caption("High-level KPI monitoring for revenue, orders, customers, and product performance")

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
    {"title": "Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💰"},
    {"title": "Orders", "value": f"{kpis['Total Orders']:,}", "icon": "🛒"},
    {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👤"},
    {"title": "Sellers", "value": f"{kpis['Total Sellers']:,}", "icon": "🏪"},
])

st.markdown("---")

monthly_revenue = monthly_sales(filtered)
monthly_orders_df = monthly_orders(filtered)
combined = monthly_revenue.merge(monthly_orders_df, on="purchase_month", how="left")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(line_chart(combined, "purchase_month", "payment_value", "Monthly Revenue"), use_container_width=True)
with col2:
    st.plotly_chart(line_chart(combined, "purchase_month", "orders", "Monthly Orders"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    category_df = revenue_by_category(filtered).head(10)
    st.plotly_chart(bar_chart(category_df.rename(columns={"payment_value": "Revenue"}), "product_category_name_english", "Revenue", "Revenue by Category"), use_container_width=True)
with col2:
    state_df = customer_state_sales(filtered).head(10)
    st.plotly_chart(bar_chart(state_df.rename(columns={"payment_value": "Revenue"}), "customer_state", "Revenue", "Revenue by State"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    products_df = top_products(filtered, top_n=10)
    st.plotly_chart(bar_chart(products_df.rename(columns={"payment_value": "Revenue", "product_id": "Product ID"}), "Product ID", "Revenue", "Top Products"), use_container_width=True)
with col2:
    sellers_df = top_sellers(filtered, top_n=10)
    st.plotly_chart(bar_chart(sellers_df.rename(columns={"payment_value": "Revenue", "seller_id": "Seller ID"}), "Seller ID", "Revenue", "Top Sellers"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    payment_df = payment_analysis(filtered)
    st.plotly_chart(bar_chart(payment_df.rename(columns={"Revenue": "Revenue"}), "payment_type", "Revenue", "Payment Distribution"), use_container_width=True)
with col2:
    review_df = review_analysis(filtered)
    st.plotly_chart(bar_chart(review_df, "review_score", "count", "Review Distribution"), use_container_width=True)

st.markdown("---")
show_table(filtered[["order_id", "customer_state", "product_category_name_english", "payment_value", "review_score", "delivery_days"]].head(20), "Executive Summary Data")
