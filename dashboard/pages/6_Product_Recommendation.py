"""Product recommendation page for the RetailIQ AI dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import get_dashboard_data, get_recommendation_assets
from src.recommendation import recommend_products

show_sidebar()

st.title("🛍 Product Recommendation")
st.caption("Discover similar products using the trained content-based recommender")

try:
    df = get_dashboard_data()
    products, vectorizer, similarity_matrix = get_recommendation_assets()
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load recommendation assets: {exc}")
    st.stop()

product_ids = sorted(products["product_id"].dropna().astype(str).tolist())
selected_product = st.selectbox("Select a product", product_ids)

if selected_product:
    recommended = recommend_products(selected_product, products, similarity_matrix, top_n=6)
    if recommended.empty:
        st.warning("No similar products were found.")
    else:
        st.success("Top similar products")
        show_table(recommended, "Recommendations")

st.markdown("---")
show_table(products.head(20), "Available Products")
