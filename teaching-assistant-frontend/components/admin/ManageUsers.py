import streamlit as st
from utils.admin_functions import get_all_users

def render():
    if "users" not in st.session_state:
        users = get_all_users()
        print(users)
    st.subheader("📚 Manage Users")
    st.write("Create, update, or delete course offerings.")
    # Example: course creation form
    with st.form("create_course"):
        name = st.text_input("Course Name")
        code = st.text_input("Course Code")
        submit = st.form_submit_button("Create Course")
    if submit:
        st.success(f"Course {code} - {name} created.")
