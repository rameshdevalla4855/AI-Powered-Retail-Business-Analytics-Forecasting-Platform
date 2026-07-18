"""Shared Plotly chart helpers for the dashboard."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def line_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a simple Plotly line chart."""
    fig = px.line(data, x=x_col, y=y_col, markers=True, title=title)
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str, color: str = "#2563eb") -> go.Figure:
    """Create a polished Plotly bar chart."""
    fig = px.bar(data, x=x_col, y=y_col, title=title, color_discrete_sequence=[color])
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def pie_chart(data: pd.DataFrame, names_col: str, values_col: str, title: str) -> go.Figure:
    """Create a Plotly pie chart."""
    fig = px.pie(data, names=names_col, values=values_col, title=title, hole=0.4)
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def scatter_chart(data: pd.DataFrame, x_col: str, y_col: str, color_col: str, title: str) -> go.Figure:
    """Create a Plotly scatter chart."""
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=title, hover_data=["customer_id"])
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    return fig
