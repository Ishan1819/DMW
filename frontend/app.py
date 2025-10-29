import streamlit as st
import requests
import pandas as pd
import base64
import io

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="AI Data Analyzer", layout="wide")
st.title("🤖 AI Data Analyzer")

# Upload dataset
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])
if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    res = requests.post(f"{API_URL}/preprocess/upload", files=files)
    data = res.json()
    st.success("✅ File Uploaded")
    st.write("Columns:", data["columns"])
    file_path = data["path"]

    # Preprocessing
    st.subheader("🧹 Preprocessing")
    technique = st.selectbox("Choose technique", ["missing_values", "encode", "outliers"])
    if st.button("Apply Preprocessing"):
        res = requests.post(f"{API_URL}/preprocess/apply", data={"file_path": file_path, "technique": technique})
        st.success(res.json()["message"])

    # Visualization
    st.subheader("📊 Visualization")
    if st.button("✨ Auto Generate 5 Charts"):
        res = requests.post(f"{API_URL}/visualize/auto", data={"file_path": file_path})
        try:
            data = res.json()
            st.code(data.get("generated_code", ""), language="python")
            # If backend returns base64 chart
            if "chart" in data:
                st.image(base64.b64decode(data["chart"]))
        except Exception:
            # If backend returns image directly
            st.image(res.content, caption="Generated Chart")

    query = st.text_input("Ask AI for Custom Chart")
    if st.button("🎨 Generate Chart"):
        res = requests.post(f"{API_URL}/visualize/chat", data={"file_path": file_path, "query": query})
        try:
            data = res.json()
            st.code(data.get("generated_code", ""), language="python")
            if "chart" in data:
                st.image(base64.b64decode(data["chart"]))
        except Exception:
            st.image(res.content, caption="Generated Chart")