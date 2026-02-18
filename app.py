import streamlit as st
import requests
import subprocess
import time
import os

# Start FastAPI backend
if "backend_started" not in st.session_state:
    subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    )
    time.sleep(5)
    st.session_state.backend_started = True


BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Study Search")

st.title("📚 Smart Study Search System")
st.write("AI-powered academic search platform")

st.divider()

#Upload
st.subheader("📂 Upload PDF")

uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])

if st.button("Upload") and uploaded_file:

    files = {
        "file": (uploaded_file.name, uploaded_file, "application/pdf")
    }

    res = requests.post(f"{BACKEND_URL}/upload/", files=files)

    if res.status_code == 200:
        st.success("Uploaded successfully!")
    else:
        st.error("Upload failed")


st.divider()

# Search 
st.subheader("🔍 Search")

query = st.text_input("Enter your question")

if st.button("Search") and query:

    res = requests.get(
        f"{BACKEND_URL}/search/",
        params={"query": query}
    )

    if res.status_code == 200:

        data = res.json()

        st.subheader("Results")

        if len(data["results"]) == 0:
            st.info("No results found")

        for i, doc in enumerate(data["results"], 1):
            st.markdown(f"### {i}. {doc['name']}")
            st.write(doc["content"] + "...")

    else:
        st.error("Search failed")

