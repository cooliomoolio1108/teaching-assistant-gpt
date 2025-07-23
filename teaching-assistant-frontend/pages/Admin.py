import streamlit as st
import requests
import os
from dotenv import load_dotenv

from utils.styling import inject_custom_css

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/embed"

inject_custom_css()
st.title("Admin Page")
st.subheader("Manage your Courses")

uploaded_files = st.file_uploader(
    "Choose files", accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Uploading and processing..."):
        # Prepare multipart-encoded file data
        files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]

        response = requests.post(API_URL, files=files)

        if response.status_code == 201:
            res = response.json()
            st.success(f"Processed {res['total_files']} files, {res['total_chunks']} chunks embedded.")
        else:
            st.error(f"Upload failed: {response.text}")