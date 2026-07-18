"""Sales forecasting page for the RetailIQ AI dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.cards import metric_row
from dashboard.components.charts import line_chart
from dashboard.components.filters import dashboard_filters
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_forecasting_model
from src.forecasting import FEATURE_COLUMNS, predict_sales

show_sidebar()

st.title("🔮 Sales Forecasting")
st.caption("Predict sales using the trained forecasting model")

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
    model = get_forecasting_model()
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load forecasting model: {exc}")
    st.stop()

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

st.subheader("Predict Sales")
with st.form("forecast_form"):
    price = st.number_input("Price", min_value=0.0, value=50.0)
    freight_value = st.number_input("Freight Value", min_value=0.0, value=10.0)
    review_score = st.number_input("Review Score", min_value=0.0, max_value=5.0, value=4.0)
    delivery_days = st.number_input("Delivery Days", min_value=0.0, value=10.0)
    delay_days = st.number_input("Delivery Delay Days", min_value=0.0, value=0.0)
    submitted = st.form_submit_button("Predict")

if submitted:
    sample_df = pd.DataFrame([{
        "price": price,
        "freight_value": freight_value,
        "review_score": review_score,
        "delivery_days": delivery_days,
        "delivery_delay_days": delay_days,
    }])
    sample_df = sample_df[[*FEATURE_COLUMNS]]
    prediction = predict_sales(model, sample_df)[0]
    st.success(f"Predicted Revenue: ${prediction:,.2f}")

st.markdown("---")

sample_history = filtered[["price", "freight_value", "review_score", "delivery_days", "delivery_delay_days", "payment_value"]].head(20)
show_table(sample_history, "Historical Features")
