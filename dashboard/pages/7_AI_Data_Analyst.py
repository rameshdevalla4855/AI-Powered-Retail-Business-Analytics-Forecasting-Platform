"""Natural language-style analytics assistant for the dashboard."""

from __future__ import annotations

import streamlit as st

from ai.analytics_router import AnalyticsRouter
from ai.business_rules import BusinessRules
from ai.chart_generator import ChartGenerator
from ai.conversation_memory import ConversationMemory
from ai.insight_generator import InsightGenerator
from ai.intent_classifier import IntentClassifier
from ai.llm_interface import LLMInterface
from ai.query_parser import QueryParser
from ai.report_generator import ReportGenerator
from dashboard.components.cards import metric_row
from dashboard.components.sidebar import show_sidebar
from dashboard.components.tables import show_table
from dashboard.utils import apply_filters, get_dashboard_data, get_kpi_summary

show_sidebar()

st.title("🤖 AI Data Analyst")
st.caption("Ask business questions in plain English and receive analytics, charts, insights, and reports")

try:
    df = get_dashboard_data()
except Exception as exc:  # pragma: no cover - UI fallback
    st.error(f"Unable to load data: {exc}")
    st.stop()

with st.sidebar:
    st.subheader("Query Controls")
    selected_states = st.multiselect("State", sorted(df["customer_state"].dropna().unique().tolist()))
    selected_categories = st.multiselect("Category", sorted(df["product_category_name_english"].dropna().unique().tolist()))

query = st.text_input("Ask a question", value="Show monthly sales")

filtered = df.copy()
if selected_states:
    filtered = filtered[filtered["customer_state"].isin(selected_states)]
if selected_categories:
    filtered = filtered[filtered["product_category_name_english"].isin(selected_categories)]

if filtered.empty:
    st.warning("No rows match the current filters.")
    st.stop()

kpis = get_kpi_summary(filtered)
metric_row([
    {"title": "Revenue", "value": f"${kpis['Total Revenue']:,.2f}", "icon": "💰"},
    {"title": "Orders", "value": f"{kpis['Total Orders']:,}", "icon": "🛒"},
    {"title": "Customers", "value": f"{kpis['Total Customers']:,}", "icon": "👥"},
])

st.markdown("---")

classifier = IntentClassifier()
router = AnalyticsRouter()
chart_generator = ChartGenerator()
insight_generator = InsightGenerator()
business_rules = BusinessRules()
query_parser = QueryParser()
report_generator = ReportGenerator()
memory = ConversationMemory()
llm = LLMInterface()

intent = classifier.classify(query)
parsed_query = query_parser.parse(query)
result, chart_type, title = router.route(filtered, intent)
fig = chart_generator.create(result, chart_type, title)
insight = insight_generator.generate(result, intent)
recommendation = business_rules.recommend(intent)
response_text = f"Intent: {intent}\n\n{llm.generate(query)}"

memory.add(query, response_text)

st.subheader(title)
st.markdown("### Summary")
st.write(f"This analysis focuses on {intent.replace('_', ' ')} and uses the current dataset filters.")
st.markdown("### KPI")
st.write({"Revenue": round(float(result["Revenue"].sum()) if "Revenue" in result.columns else float(filtered["payment_value"].sum()), 2)})
st.markdown("### Table")
show_table(result, title)
st.markdown("### Plotly Chart")
st.plotly_chart(fig, use_container_width=True)
st.markdown("### Business Insight")
st.info(insight)
st.markdown("### Recommendation")
st.success(recommendation)

st.markdown("---")

with st.expander("Recent queries"):
    for item in memory.recent(5):
        st.write(f"- {item['query']}")

csv_data = report_generator.to_csv(result)
excel_data = report_generator.to_excel(result)

st.download_button("Download CSV", csv_data, file_name="ai_analysis.csv", mime="text/csv")
st.download_button("Download Excel", excel_data, file_name="ai_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

