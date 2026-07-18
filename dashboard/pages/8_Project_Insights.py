"""Project insights page for the RetailIQ AI dashboard."""

from __future__ import annotations

import streamlit as st

from dashboard.components.sidebar import show_sidebar

st.set_page_config(page_title="Project Insights", page_icon="💡", layout="wide")
show_sidebar()

st.title("💡 Project Insights")
st.caption("Executive summary of the analytics workflow, model performance, and recommendations")

st.subheader("Business Conclusions")
st.markdown("- Revenue performance is driven by high-value categories and a small set of top-selling products.\n- Customer retention can be improved by focusing on repeat buyers and state-specific offers.\n- Delivery reliability and review quality strongly influence customer satisfaction.")

st.subheader("EDA Summary")
st.markdown("- The processed dataset contains enriched features such as delivery days, review score, and customer-level aggregates.\n- Revenue is concentrated across a limited number of categories and sellers.\n- Seasonal purchasing behavior is visible in the monthly transaction trends.")

st.subheader("Machine Learning Summary")
st.markdown("- A forecasting model estimates revenue using pricing, delivery, and review-based features.\n- Customer segmentation groups customers into meaningful clusters using spend, delivery, and review behavior.\n- Product recommendation uses content-based similarity to surface relevant alternatives.")

st.subheader("Recommendations")
st.markdown("- Prioritize inventory planning for top categories.\n- Improve delivery speed for high-value orders.\n- Use segmentation insights to personalize engagement campaigns.")

st.subheader("Future Scope")
st.markdown("- Connect the AI analyst to an LLM backend for natural language conversations.\n- Add real-time data connectors to operational systems.\n- Extend forecasting to daily and promotional planning scenarios.")
