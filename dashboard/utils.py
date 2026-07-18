"""Shared utilities for the Streamlit dashboard."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd
import streamlit as st

from src.analytics import get_kpis
from src.data_loader import load_processed_dataset
from src.forecasting import load_model as load_forecasting_model
from src.recommendation import load_recommendation_model
from src.segmentation import load_segmentation_model
from src.utils import format_currency, validate_dataframe


@lru_cache(maxsize=1)
def _load_dashboard_frame() -> pd.DataFrame:
    """Load and validate the processed dataset once per Python process."""
    df = load_processed_dataset()
    validate_dataframe(df)
    return df


def load_data() -> pd.DataFrame:
    """Return a shared dataframe for the current browser session."""
    if "dashboard_df" not in st.session_state:
        st.session_state["dashboard_df"] = _load_dashboard_frame()
    return st.session_state["dashboard_df"]


def get_dashboard_data() -> pd.DataFrame:
    """Return a validated dataframe or stop the app gracefully."""
    try:
        return load_data()
    except Exception as exc:  # pragma: no cover - UI fallback
        st.error(f"Unable to load the dashboard dataset: {exc}")
        st.stop()


def apply_filters(
    df: pd.DataFrame,
    date_range: tuple | None = None,
    states: list[str] | None = None,
    categories: list[str] | None = None,
    sellers: list[str] | None = None,
    payment_types: list[str] | None = None,
) -> pd.DataFrame:
    """Filter the dataset using the common dashboard controls."""
    filtered = df.copy()

    if date_range:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["order_purchase_timestamp"] >= pd.Timestamp(start_date))
            & (filtered["order_purchase_timestamp"] <= pd.Timestamp(end_date))
        ]

    if states:
        filtered = filtered[filtered["customer_state"].isin(states)]

    if categories:
        filtered = filtered[filtered["product_category_name_english"].isin(categories)]

    if sellers:
        filtered = filtered[filtered["seller_id"].isin(sellers)]

    if payment_types:
        filtered = filtered[filtered["payment_type"].isin(payment_types)]

    return filtered


@st.cache_data(show_spinner=False, ttl=600)
def get_kpi_summary(df: pd.DataFrame) -> dict:
    """Cache KPI calculations for repeat use across pages."""
    return get_kpis(df)


@lru_cache(maxsize=1)
def _load_forecasting_model_cached():
    """Load the forecasting model once per Python process."""
    return load_forecasting_model("sales_forecasting_model.pkl")


@lru_cache(maxsize=1)
def _load_recommendation_assets_cached():
    """Load recommendation assets once per Python process."""
    return load_recommendation_model()


@lru_cache(maxsize=1)
def _load_segmentation_assets_cached():
    """Load segmentation assets once per Python process."""
    return load_segmentation_model()


def get_forecasting_model():
    """Return the shared forecasting model for the current session."""
    if "forecasting_model" not in st.session_state:
        st.session_state["forecasting_model"] = _load_forecasting_model_cached()
    return st.session_state["forecasting_model"]


def get_recommendation_assets():
    """Return the shared recommendation assets for the current session."""
    if "recommendation_assets" not in st.session_state:
        st.session_state["recommendation_assets"] = _load_recommendation_assets_cached()
    return st.session_state["recommendation_assets"]


def get_segmentation_assets():
    """Return the shared segmentation assets for the current session."""
    if "segmentation_assets" not in st.session_state:
        st.session_state["segmentation_assets"] = _load_segmentation_assets_cached()
    return st.session_state["segmentation_assets"]


__all__ = [
    "apply_filters",
    "format_currency",
    "get_dashboard_data",
    "get_forecasting_model",
    "get_kpi_summary",
    "get_recommendation_assets",
    "get_segmentation_assets",
    "load_data",
]