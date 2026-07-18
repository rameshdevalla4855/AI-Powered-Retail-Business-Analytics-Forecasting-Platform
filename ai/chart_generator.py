"""Generate Plotly charts for the AI assistant responses."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class ChartGenerator:
    """Create chart objects from routed analytics results."""

    def __init__(self) -> None:
        self.template = "plotly_white"

    def create(self, data: pd.DataFrame, chart_type: str, title: str) -> go.Figure:
        """Create a Plotly chart based on the requested chart type."""
        try:
            if chart_type == "line":
                x_col = data.columns[0]
                y_col = data.columns[-1]
                fig = px.line(data, x=x_col, y=y_col, markers=True, title=title)
            elif chart_type == "bar":
                x_col = data.columns[0]
                y_col = data.columns[-1]
                fig = px.bar(data, x=x_col, y=y_col, title=title)
            elif chart_type == "pie":
                names_col = data.columns[0]
                values_col = data.columns[-1]
                fig = px.pie(data, names=names_col, values=values_col, title=title, hole=0.4)
            else:
                fig = go.Figure(
                    data=[
                        go.Table(
                            header=dict(
                                values=list(data.columns),
                                fill_color="#F0F2F6",
                                align="left",
                                font=dict(color="#2E4057", size=12),
                            ),
                            cells=dict(
                                values=[data[col] for col in data.columns],
                                fill_color="white",
                                align="left",
                                font=dict(color="#2E4057", size=11),
                            ),
                        )
                    ]
                )
                fig.update_layout(title=title)
        except Exception:
            fig = go.Figure()
            fig.add_annotation(text="Chart unavailable for this result.", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(title=title)

        fig.update_layout(template=self.template, margin=dict(l=10, r=10, t=40, b=10))
        return fig
