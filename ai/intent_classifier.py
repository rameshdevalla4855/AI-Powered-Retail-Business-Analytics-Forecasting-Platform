"""Rule-based intent classification for retail analytics queries."""

from __future__ import annotations

import re
from typing import Any


class IntentClassifier:
    """Classify a natural language query into a supported analytics intent."""

    def __init__(self) -> None:
        self.patterns = {
            "monthly_sales": [r"monthly sales", r"sales trend", r"revenue trend", r"monthly revenue"],
            "top_products": [r"top products", r"best products", r"popular products", r"product performance"],
            "revenue_by_state": [r"revenue by state", r"highest revenue state", r"best state", r"state performs"],
            "payment_analysis": [r"payment", r"payment type", r"payment distribution"],
            "top_customers": [r"top customers", r"best customers", r"high value customers", r"loyal customers"],
            "delivery_analysis": [r"delivery", r"delay", r"delivery delay", r"delivery performance"],
            "review_analysis": [r"review", r"review score", r"customer feedback"],
            "forecast": [r"forecast", r"predict", r"expected demand", r"next month"],
            "segmentation": [r"segment", r"segmentation", r"cluster", r"customer segment"],
            "recommendation": [r"recommend", r"similar products", r"suggest alternatives", r"find similar"],
            "category_analysis": [r"category", r"categories", r"top categories"],
            "executive_summary": [r"summary", r"executive summary", r"business summary"],
        }

    def classify(self, query: str) -> str:
        """Return the best matching intent for the query."""
        normalized = query.lower().strip()
        for intent, patterns in self.patterns.items():
            if any(re.search(pattern, normalized) for pattern in patterns):
                return intent
        return "general"

    def describe(self, query: str) -> dict[str, Any]:
        """Return a structured intent description used by the assistant."""
        return {"intent": self.classify(query), "query": query}
