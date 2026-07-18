"""Customer segmentation page for the RetailIQ AI dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.cards import metric_row
from dashboard.components.charts import bar_chart, scatter_chart
from dashboard.components.filters import dashboard_filters
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_segmentation_assets
from src.segmentation import cluster_summary, predict_customer_segment, prepare_customer_data

st.set_page_config(page_title="Customer Segmentation", page_icon="🧠", layout="wide")
show_sidebar()

st.title("🧠 Customer Segmentation")
st.caption("Cluster distribution, characteristic profiles, and cluster prediction")

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
    model, scaler = get_segmentation_assets()
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load segmentation assets: {exc}")
    st.stop()

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

customer_df = prepare_customer_data(filtered)
customer_df["Cluster"] = customer_df[["TotalSpent", "AvgDelivery", "AvgReview"]].apply(
    lambda row: predict_customer_segment(model, scaler, row["TotalSpent"], row["AvgDelivery"], row["AvgReview"]), axis=1
)
summary = cluster_summary(customer_df)

metric_row([
    {"title": "Clusters", "value": f"{summary['Cluster'].nunique()}", "icon": "🎯"},
    {"title": "Customers", "value": f"{customer_df['customer_id'].nunique()}", "icon": "👥"},
    {"title": "Top Cluster", "value": str(summary.sort_values('Customers', ascending=False)['Cluster'].iloc[0]), "icon": "📌"},
])

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(summary, "Cluster", "Customers", "Cluster Distribution"), use_container_width=True)
with col2:
    st.plotly_chart(scatter_chart(customer_df, "AvgDelivery", "TotalSpent", "Cluster", "Cluster Characteristics"), use_container_width=True)

st.markdown("---")

st.subheader("Predict a New Customer Cluster")
with st.form("cluster_form"):
    total_spent = st.number_input("Total Spent", min_value=0.0, value=100.0)
    delivery_days = st.number_input("Average Delivery Days", min_value=0.0, value=10.0)
    review_score = st.number_input("Average Review Score", min_value=0.0, max_value=5.0, value=4.0)
    submitted = st.form_submit_button("Predict Cluster")

if submitted:
    cluster = predict_customer_segment(model, scaler, total_spent, delivery_days, review_score)
    st.success(f"Predicted cluster: {cluster}")

st.markdown("---")
show_table(summary, "Cluster Summary")
