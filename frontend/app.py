import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Cloud Cost Analyzer", layout="wide")

st.title("☁️ AI Cloud Cost Analyzer Dashboard")

API_URL = "http://3.84.227.142:8000"

# ======================
# 💰 COST SECTION
# ======================
st.header("💰 AWS Cost Data")

try:
    cost_response = requests.get(f"{API_URL}/cost").json()

    df = pd.DataFrame(cost_response["data"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Cost Table")
        st.dataframe(df)

    with col2:
        st.subheader("💰 Total Cost")
        st.metric("Total AWS Cost", f"${cost_response['total_cost']}")

except Exception as e:
    st.error(f"Cost API Error: {e}")

# ======================
# 🤖 AI SECTION
# ======================
st.header("🤖 AI Insights & Prediction")

try:
    ai_response = requests.get(f"{API_URL}/ai-analysis").json()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📈 Predicted Next Month Cost")
        st.metric(
            "Prediction",
            f"${ai_response['predicted_next_month_cost']:.2f}"
        )

    with col4:
        st.subheader("🧠 AI Insights")

        for insight in ai_response["insights"]:
            st.write("👉", insight)

except Exception as e:
    st.warning("AI endpoint not ready or backend error")
