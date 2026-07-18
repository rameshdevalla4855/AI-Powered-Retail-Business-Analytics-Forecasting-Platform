"""Reusable KPI card helpers for the dashboard."""

from typing import Optional

import streamlit as st


def metric_card(title: str, value: str, delta: Optional[str] = None, icon: str = "📈") -> None:
    """Render a polished metric card inside a Streamlit container."""
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e6eaf1; border-radius:12px; padding:14px; background:linear-gradient(135deg, #f8fbff, #ffffff); margin-bottom:10px;">
                <div style="font-size:0.85rem; color:#6b7280;">{icon} {title}</div>
                <div style="font-size:1.6rem; font-weight:700; color:#111827; margin-top:6px;">{value}</div>
                <div style="font-size:0.85rem; color:#2563eb; margin-top:4px;">{delta or ''}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def metric_row(metrics: list[dict]) -> None:
    """Render a row of metric cards with consistent sizing."""
    cols = st.columns(len(metrics))
    for column, metric in zip(cols, metrics):
        with column:
            metric_card(metric["title"], metric["value"], metric.get("delta"), metric.get("icon", "📊"))