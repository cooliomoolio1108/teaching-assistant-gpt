import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime
import time
from dotenv import load_dotenv
from utils.styling import inject_custom_css
from utils.admin_functions import get_files, is_safe_folder_name, get_course, upload_files

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/files"

if "upload_done" not in st.session_state:
    st.session_state.upload_done = False

inject_custom_css()
def EmbeddingPopUp(course_id):
    if st.session_state.courses:
        courses = st.session_state.courses
        course = next((item for item in courses if item.get("id") == course_id), None)
        course_name = course["course_name"]
    if is_safe_folder_name(course_id):
        NEW_DOCUMENTS_DIR = os.path.join(DOCUMENTS_DIR, f'{course_id}')
        os.makedirs(NEW_DOCUMENTS_DIR, exist_ok=True)
    st.write(f'### Files')
    params = dict(st.query_params)
    course_id = params.get("course_id")
    print("PARAMS: ", params)
    if not st.session_state.upload_done:
        with st.container():
            uploaded_files = st.file_uploader(
                f'Upload Files for {course_name}', accept_multiple_files=True
            )
        if uploaded_files:
            st.write(f"Detected {len(uploaded_files)} file(s).")
            with st.spinner("Uploading and processing..."):
                for uploaded_file in uploaded_files:
                    files = {
                        "file": (uploaded_file.name, uploaded_file, "application/pdf"),
                        "course_id": course_id
                    }
                    data = {
                        "file_name": uploaded_file.name,
                        "path": "/test",
                        "uploaded_by": st.session_state.get("username", "unknown"),
                        "course_id": course_id,
                        "file_size": uploaded_file.size
                    }
                    try:
                        response = upload_files(data, files)
                    except Exception as e:
                        st.error(f'Error saving meta data for {uploaded_file.name}: {e}')
                    # files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
                    st.success(f"✅ {uploaded_file.name} uploaded.")
            time.sleep(3)
            st.session_state.upload_done = True
            st.rerun()
    else:
        st.info("✅ Documents successfully uploaded and processed.")
        if st.button("Upload more"):
            st.session_state.upload_done = False
            st.rerun()

def File_Display():
    params = dict(st.query_params)
    course_id = params.get("course_id")
    files = get_files(course_id)
    df = pd.DataFrame(files)
    print(df)
    # Sidebar filtering (optional)
    # st.sidebar.header("Filters")
    # uploader_filter = st.sidebar.selectbox("Uploaded by", ["All"] + sorted(df["uploaded_by"].unique().tolist()))
    # if uploader_filter != "All":
    #     df = df[df["uploaded_by"] == uploader_filter]

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