import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from utils.styling import inject_custom_css
from utils.admin_functions import get_files

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/embed"

if "upload_done" not in st.session_state:
    st.session_state.upload_done = False

inject_custom_css()
def EmbeddingPopUp():
    st.write(f'### Files')
    params = st.query_params
    print("PARAMS: ", params)
    if not st.session_state.upload_done:
        with st.container():
            uploaded_files = st.file_uploader(
                "Choose files", accept_multiple_files=True
            )

        if uploaded_files:
            st.write(f"Detected {len(uploaded_files)} file(s).")
            with st.spinner("Uploading and processing..."):
                for uploaded_file in uploaded_files:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_path = os.path.join(DOCUMENTS_DIR, f"{timestamp}_{uploaded_file.name}")

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"✅ {uploaded_file.name} uploaded.")
                    # files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
    else:
        st.info("✅ Documents successfully uploaded and processed.")
        if st.button("Upload more"):
            st.session_state.upload_done = False

def File_Display():
    files = get_files()
    df = pd.DataFrame(files)

    # Sidebar filtering (optional)
    st.sidebar.header("Filters")
    uploader_filter = st.sidebar.selectbox("Uploaded by", ["All"] + sorted(df["uploaded_by"].unique().tolist()))
    if uploader_filter != "All":
        df = df[df["uploaded_by"] == uploader_filter]

    # Show as table with action buttons
    for i, row in df.iterrows():
        with st.expander(f"{row['file_name']}"):
            st.write(f"**Uploaded by:** {row['uploaded_by']}")
            st.write(f"**Uploaded at:** {row['uploaded_at']}")
            st.write(f"**Embedded:** {'✅' if row['embedded'] else '❌'}")
            
            # col1, col2, col3 = st.columns(3)
            # with col1:
            #     if st.button("📄 View", key=f"view_{i}"):
            #         st.info(f"Simulate viewing: `{row['path']}`")
            # with col2:
            #     if st.download_button("⬇️ Download", data=open(row["path"], "rb").read(), file_name=row["file_name"]):
            #         st.success(f"Downloaded `{row['file_name']}`")
            # with col3:
            #     if st.button("🗑️ Delete", key=f"delete_{i}"):
            #         st.warning(f"Simulate deletion of `{row['file_name']}`")
            #         # Add DB/FS delete logic here