"""Route analytics intents to the existing project analytics functions."""

from __future__ import annotations

import pandas as pd

from src.analytics import (
    monthly_sales,
    payment_analysis,
    review_analysis,
    top_products,
    top_sellers,
)


class AnalyticsRouter:
    """Map a classified intent to a dataframe result and chart metadata."""

    def __init__(self) -> None:
        self.intent_handlers = {
            "monthly_sales": self._monthly_sales,
            "top_products": self._top_products,
            "revenue_by_state": self._revenue_by_state,
            "payment_analysis": self._payment_analysis,
            "top_customers": self._top_customers,
            "delivery_analysis": self._delivery_analysis,
            "review_analysis": self._review_analysis,
            "forecast": self._forecast,
            "segmentation": self._segmentation,
            "recommendation": self._recommendation,
            "category_analysis": self._category_analysis,
            "executive_summary": self._executive_summary,
        }

    def route(self, df: pd.DataFrame, intent: str) -> tuple[pd.DataFrame, str, str]:
        """Return a dataframe, chart type, and summary title for an intent."""
        if intent not in self.intent_handlers:
            return df.head(10), "table", "General Analysis"
        return self.intent_handlers[intent](df)

    def _monthly_sales(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = monthly_sales(df)
        return result, "line", "Monthly Sales Trend"

    def _top_products(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = top_products(df, top_n=10)
        result = result.rename(columns={"payment_value": "Revenue"})
        return result, "bar", "Top Products"

    def _revenue_by_state(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df.groupby("customer_state")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
        result = result.rename(columns={"payment_value": "Revenue"})
        return result, "bar", "Revenue by State"

    def _payment_analysis(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = payment_analysis(df)
        return result, "pie", "Payment Distribution"

    def _top_customers(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df.groupby("customer_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False).head(10)
        result = result.rename(columns={"payment_value": "Revenue"})
        return result, "bar", "Top Customers"

    def _delivery_analysis(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df[["delivery_days", "delivery_delay_days"]].describe().T.reset_index()
        result = result.rename(columns={"index": "Metric"})
        return result, "bar", "Delivery Performance"

    def _review_analysis(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = review_analysis(df)
        return result, "bar", "Review Distribution"

    def _forecast(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df[["purchase_month", "payment_value"]].groupby("purchase_month").sum().reset_index()
        return result, "line", "Forecast View"

    def _segmentation(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df.groupby("customer_state").size().reset_index(name="Customers")
        return result, "bar", "Customer Segmentation"

    def _recommendation(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df[["product_id", "product_category_name_english"]].drop_duplicates().head(10)
        return result, "table", "Product Recommendations"

    def _category_analysis(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df.groupby("product_category_name_english")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False).head(10)
        result = result.rename(columns={"payment_value": "Revenue"})
        return result, "bar", "Top Categories"

    def _executive_summary(self, df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
        result = df[["payment_value", "order_id"]].copy()
        result["Revenue"] = result["payment_value"]
        return result.head(10), "table", "Executive Summary"
