import streamlit as st
from utils.admin_functions import get_all_courses

def render():
    st.write('# Your Courses')
    if "courses" not in st.session_state:
        st.session_state.courses = get_all_courses()
    
    courses = st.session_state.courses

    if courses:
        if isinstance(courses, list):
            for course in courses:
                with st.container():
                    cols = st.columns([3, 2, 2, 2, 1])
                    cols[0].markdown(f"📘 **{course['course_name']}**  \n`{course['course_code']}`")
                    cols[1].markdown(f"👤 {course['coordinator']}")
                    cols[2].markdown(f"📅 Sem: `{course['sem']}`")
                    cols[3].markdown(f"🕒 Created: `{course['created_at'][:10]}`")
                    if cols[4].button("Manage", key=f'course_{course}'):
                        st.query_params.update({"course_id":course['id']})
                        st.rerun
                    