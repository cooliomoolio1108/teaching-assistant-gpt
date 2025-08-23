import streamlit as st
import os
from dotenv import load_dotenv
from utils.styling import inject_custom_css
from utils.admin_functions import get_all_courses
from utils.auth import require_login
from components import course_list
from components.admin import CourseDetails
from components.admin.Embedding import EmbeddingPopUp, File_Display
from components.PromptEngineer import render

require_login()
st.set_page_config(page_title="Chat Panel", layout="wide")
inject_custom_css()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

load_dotenv()
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
    if courses:
        course_chosen = course_list.render(courses)
        if course_chosen:
            st.session_state.view = "chosen"
            st.session_state.course_details = course_chosen
            st.rerun()

elif st.session_state.view == "chosen":
    with st.spinner("Loading..."):
        view = st.session_state.course_details
        CourseDetails.render(str(view))
        EmbeddingPopUp(str(view))
        File_Display()

        render()
