"""Business rules for retail analytics reasoning."""

from __future__ import annotations


class BusinessRules:
    """Return sensible recommendations for common retail scenarios."""

    def recommend(self, intent: str) -> str:
        """Return a recommendation based on the detected intent."""
        recommendations = {
            "monthly_sales": "Review the strongest and weakest months and align inventory and promotions accordingly.",
            "top_products": "Prioritize top-selling products in promotions and ensure stock availability.",
            "revenue_by_state": "Direct additional marketing spend toward the highest-revenue regions.",
            "payment_analysis": "Simplify the payment experience for the dominant methods used by customers.",
            "top_customers": "Create loyalty offers and personalized campaigns for your best customers.",
            "delivery_analysis": "Improve fulfillment bottlenecks that introduce the biggest delivery delays.",
            "review_analysis": "Address the main review themes to improve customer experience and satisfaction.",
            "forecast": "Plan staffing and replenishment using the forecasted demand trend.",
            "segmentation": "Tailor marketing and product mix by cluster profile.",
            "recommendation": "Recommend similar products in the same category to increase basket size.",
        }
        return recommendations.get(intent, "Continue investigating the trend and translate it into a business action plan.")
