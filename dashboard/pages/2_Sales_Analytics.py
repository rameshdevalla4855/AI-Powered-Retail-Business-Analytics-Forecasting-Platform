"""Sales analytics page for the RetailIQ AI dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.cards import metric_card, metric_row
from dashboard.components.charts import bar_chart, line_chart, pie_chart
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
    top_products,
    top_sellers,
)

show_sidebar()

st.title("📈 Sales Analytics")
st.caption("Revenue trends, product performance, and customer purchase patterns")

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
    {"title": "Average Order Value", "value": f"${kpis['Average Order Value']:,.2f}", "icon": "📊"},
    {"title": "Average Review Score", "value": f"{kpis['Average Review Score']:.1f}", "icon": "⭐"},
])

st.markdown("---")

sales_monthly = monthly_sales(filtered)
orders_monthly = monthly_orders(filtered)
monthly = sales_monthly.merge(orders_monthly, on="purchase_month", how="left")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(line_chart(monthly, "purchase_month", "payment_value", "Monthly Revenue"), use_container_width=True)
with col2:
    st.plotly_chart(line_chart(monthly, "purchase_month", "orders", "Monthly Orders"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    category_revenue = (
        filtered.groupby("product_category_name_english")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
        .head(10)
    )
    st.plotly_chart(bar_chart(category_revenue, "product_category_name_english", "payment_value", "Top Categories"), use_container_width=True)
with col2:
    payment = payment_analysis(filtered)
    st.plotly_chart(pie_chart(payment, "payment_type", "Revenue", "Payment Distribution"), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    top_products_df = top_products(filtered, top_n=10)
    st.plotly_chart(bar_chart(top_products_df.rename(columns={"payment_value": "Revenue", "product_id": "Product ID"}), "Product ID", "Revenue", "Top Products"), use_container_width=True)
with col2:
    top_sellers_df = top_sellers(filtered, top_n=10)
    st.plotly_chart(bar_chart(top_sellers_df.rename(columns={"payment_value": "Revenue", "seller_id": "Seller ID"}), "Seller ID", "Revenue", "Top Sellers"), use_container_width=True)

st.markdown("---")

st.subheader("Delivery and Review Performance")
col1, col2 = st.columns(2)
with col1:
    delivery_summary = pd.DataFrame({
        "Metric": ["Average Delivery Days", "Average Delay", "Maximum Delay"],
        "Value": [filtered["delivery_days"].mean(), filtered["delivery_delay_days"].mean(), filtered["delivery_delay_days"].max()],
    })
    st.dataframe(delivery_summary, use_container_width=True)
with col2:
    review = review_analysis(filtered)
    st.plotly_chart(bar_chart(review, "review_score", "count", "Review Distribution"), use_container_width=True)

st.markdown("---")

show_table(payment_analysis(filtered), "Payment Analysis")
show_table(top_products(filtered, top_n=10), "Top Products")
