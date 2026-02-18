import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Study Search", layout="centered")

# Title
st.title("📚 Smart Study Search System")
st.write("AI-powered search for college study materials")

st.divider()

# Upload Section 
st.subheader("📂 Upload Study Material")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if st.button("Upload") and uploaded_file is not None:

    files = {
        "file": (uploaded_file.name, uploaded_file, "application/pdf")
    }

    with st.spinner("Uploading..."):
        response = requests.post(
            f"{BACKEND_URL}/upload/",
            files=files
        )

    if response.status_code == 200:
        st.success("File uploaded successfully!")
    else:
        st.error("Upload failed")


st.divider()

# Search Section 
st.subheader("🔍 Search Your Doubt")

query = st.text_input("Enter your question")

if st.button("Search") and query:

    params = {
        "query": query
    }

    with st.spinner("Searching..."):
        response = requests.get(
            f"{BACKEND_URL}/search/",
            params=params
        )

    if response.status_code == 200:

        data = response.json()
        results = data["results"]

        st.subheader("📄 Results")

        if len(results) == 0:
            st.info("No matching documents found")

        for i, doc in enumerate(results, 1):
            st.markdown(f"### {i}. {doc['name']}")
            st.write(doc["content"] + "...")

    else:
        st.error("Search failed")
