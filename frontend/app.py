import streamlit as st
import requests
import pandas as pd

st.title("☁️ AI Cloud Cost Analyzer Dashboard")

API_URL = "http://3.84.227.142:8000/cost"

st.write("Fetching AWS cost data...")

try:
    response = requests.get(API_URL)
    data = response.json()

    df = pd.DataFrame(data["data"])

    st.subheader("📊 Cost Table")
    st.dataframe(df)

    st.subheader("💰 Total Cost")
    st.metric("Total AWS Cost", f"${data['total_cost']}")

except Exception as e:
    st.error(f"Error fetching data: {e}")
