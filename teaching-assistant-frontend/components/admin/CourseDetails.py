import streamlit as st
from typing import Dict
from utils.admin_functions import get_course

def reset_view():
    st.session_state.update({
        "view": "main",
        "course_id": None,
        "upload_done": False
    })

def render(course_id: str):
    if "editable" not in st.session_state:
        st.session_state.editable = False

    if "current_course" not in st.session_state:
        st.session_state.current_course = get_course(course_id)

    course = get_course(course_id)

    st.button("↩", on_click=reset_view)
    
    if isinstance(course, list) and course and isinstance(course[0], dict):
        details = course[0]
        st.title(f'{details.get("course_code", "Nil")}: {details.get("course_name", "Untitled")}')
        editable = st.session_state.editable
        if not editable:
            if st.button("✎", key="edit_toggle_button_on"):
                st.session_state.editable = True
                st.rerun()
        else:
            if st.button("❌", key="edit_toggle_button_off"):
                st.session_state.editable = False
                st.rerun()
        with st.form("edit_course_form" if editable else "view_course_form"):
            name = st.text_input("Course Name", value=details.get("course_name", ""), disabled=not editable)
            code = st.text_input("Course Code", value=details.get("course_code", ""), disabled=not editable)
            sem = st.text_input("Available Semesters", value=details.get("sem", ""), disabled=not editable)
            coordinator = st.text_input("Course Name", value=details.get("coordinator", ""), disabled=not editable)
            if editable:
                submitted = st.form_submit_button("Submit")
                st.session_state.editable = False
            else:
                st.form_submit_button("Click edit icon to edit", disabled=True)
    else:
        st.write("Course Failed to Load!")