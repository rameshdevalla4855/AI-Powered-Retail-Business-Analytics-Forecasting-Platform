"""Reusable table helpers for dashboard results."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def show_table(data: pd.DataFrame, title: str = "Results") -> None:
    """Display a dataframe table with a title."""
    if data.empty:
        st.info("No data available for the selected view.")
        return
    st.subheader(title)
    st.dataframe(data.head(50), use_container_width=True)
