import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Cloud Cost Analyzer", layout="wide")
st.title("☁️ AI Cloud Cost Analyzer Dashboard")

API_URL = os.environ.get("API_URL", "http://3.84.227.142:8000")

# Fetch data from both endpoints
try:
    cost_response = requests.get(f"{API_URL}/cost", timeout=10).json()
    ai_response = requests.get(f"{API_URL}/ai-analysis", timeout=30).json()
except Exception as e:
    st.error(f"Cannot connect to backend API: {e}")
    st.stop()

df = pd.DataFrame(cost_response["data"])
monthly_costs = ai_response["current_month_costs"]
predicted = ai_response["predicted_next_month_cost"]
insights = ai_response["insights"]

# ── Top metrics ───────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Spend", f"${cost_response['total_cost']:,.2f}")
with col2:
    avg = sum(monthly_costs) / len(monthly_costs)
    st.metric("Monthly Average", f"${avg:,.2f}")
with col3:
    delta = predicted - monthly_costs[-1]
    st.metric("Predicted Next Month", f"${predicted:,.2f}", delta=f"${delta:+.2f}")

st.divider()

# ── Charts ────────────────────────────────────────────────
col4, col5 = st.columns(2)

with col4:
    st.subheader("📈 Monthly Cost Trend")
    monthly_df = df.groupby("month")["cost"].sum().reset_index().sort_values("month")
    fig_trend = px.line(
        monthly_df, x="month", y="cost",
        markers=True,
        labels={"month": "Month", "cost": "Cost (USD)"}
    )
    fig_trend.update_traces(line_color="#1f77b4", line_width=2, marker_size=6)
    fig_trend.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_trend, use_container_width=True)

with col5:
    st.subheader("🗂️ Cost by Service")
    service_df = df.groupby("service")["cost"].sum().reset_index()
    fig_pie = px.pie(
        service_df, names="service", values="cost",
        hole=0.4
    )
    fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── Table + Insights ──────────────────────────────────────
col6, col7 = st.columns(2)

with col6:
    st.subheader("📋 Cost Breakdown")
    st.dataframe(df, use_container_width=True, hide_index=True)

with col7:
    st.subheader("🤖 AI Insights")
    for insight in insights:
        st.info(insight)

st.divider()

# ── AI Chatbot ────────────────────────────────────────────
st.subheader("💬 Ask AI About Your Costs")
st.caption("Ask anything about your AWS spending — e.g. 'Which service costs the most?' or 'How can I reduce my bill?'")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about your AWS costs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"question": prompt},
                    timeout=30
                ).json()
                answer = res.get("answer", "No response received.")
            except Exception as e:
                answer = f"Could not reach AI service: {e}"
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
