import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.styling import inject_custom_css
from utils.admin_functions import get_all_courses
from components import course_list
from components.admin import CourseDetails
from components.admin.Embedding import EmbeddingPopUp, File_Display

inject_custom_css()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/embed"
st.set_page_config(page_title="Course Panel", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "main"
    
if "upload_done" not in st.session_state:
    st.session_state.upload_done = False

if st.session_state.view == "main":  
    st.write('# Your Courses')
    st.markdown("<br><br>", unsafe_allow_html=True) 
    if "courses" not in st.session_state:
        st.session_state.courses = get_all_courses()

    courses = st.session_state.courses

    @st.dialog("Embedding")
    def Embeddings():
        st.title("Embedding Page")
        st.subheader("Manage your Courses")

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

    if courses:
        course_chosen = course_list.render(courses, Embeddings)
        if course_chosen:
            st.session_state.view = "chosen"
            st.session_state.course_details = course_chosen
            st.rerun()

elif st.session_state.view == "chosen":
    view = st.session_state.course_details
    CourseDetails.render(str(view))
    EmbeddingPopUp(str(view))
    File_Display()
