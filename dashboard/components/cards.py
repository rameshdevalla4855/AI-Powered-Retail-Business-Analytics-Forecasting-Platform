"""Reusable KPI card helpers for the dashboard."""

from typing import Optional

import streamlit as st


def metric_card(title: str, value: str, delta: Optional[str] = None, icon: str = "📈") -> None:
    """Render a polished metric card inside a Streamlit container."""
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #dbeafe; border-radius:14px; padding:14px 16px; background:linear-gradient(135deg, #f8fbff, #ffffff); margin-bottom:10px; box-shadow:0 4px 12px rgba(15,23,42,0.04);">
                <div style="font-size:0.82rem; color:#64748b; text-transform:uppercase; letter-spacing:0.04em;">{icon} {title}</div>
                <div style="font-size:1.55rem; font-weight:700; color:#0f172a; margin-top:6px;">{value}</div>
                <div style="font-size:0.86rem; color:#2563eb; margin-top:4px;">{delta or ''}</div>
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


def module_card(title: str, description: str, icon: str, page_name: str) -> None:
    """Render a polished module launch card with a lightweight navigation link."""
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #dbeafe; border-radius:14px; padding:14px 16px; background:linear-gradient(135deg, #ffffff, #f8fbff); margin-bottom:10px; min-height:130px;">
                <div style="font-size:1.1rem; font-weight:700; color:#0f172a;">{icon} {title}</div>
                <div style="font-size:0.92rem; color:#475569; margin-top:8px; line-height:1.5;">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(page_name, label="Open module →")