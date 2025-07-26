import streamlit as st

def render():
    st.subheader("📚 Manage Courses")
    st.write("Create, update, or delete course offerings.")
    # Example: course creation form
    with st.form("create_course"):
        name = st.text_input("Course Name")
        code = st.text_input("Course Code")
        submit = st.form_submit_button("Create Course")
    if submit:
        st.success(f"Course {code} - {name} created.")
