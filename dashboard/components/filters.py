"""Reusable filter controls for dashboard pages."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


def dashboard_filters(df: pd.DataFrame) -> dict[str, Any]:
    """Render common dashboard filters and return selected values."""
    st.sidebar.subheader("Filters")

    date_col = df["order_purchase_timestamp"]
    min_date = date_col.min().date()
    max_date = date_col.max().date()
    start_date, end_date = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    state_options = sorted(df["customer_state"].dropna().unique().tolist())
    selected_states = st.sidebar.multiselect("State", state_options, default=state_options)

    category_options = sorted(df["product_category_name_english"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", category_options, default=category_options)

    seller_options = sorted(df["seller_id"].dropna().unique().tolist())
    selected_sellers = st.sidebar.multiselect("Seller", seller_options, default=seller_options)

    payment_options = sorted(df["payment_type"].dropna().unique().tolist())
    selected_payment_types = st.sidebar.multiselect("Payment Type", payment_options, default=payment_options)

    return {
        "date_range": (start_date, end_date),
        "states": selected_states,
        "categories": selected_categories,
        "sellers": selected_sellers,
        "payment_types": selected_payment_types,
    }
