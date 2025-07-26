import streamlit as st
from utils.styling import inject_custom_css
from components.admin import ManageCourses, ManageUsers
inject_custom_css()

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("Admin Dashboard")

if "admin_view" not in st.session_state:
    st.session_state.admin_view = "Home"

with st.sidebar:
    st.header("Admin Functions")
    if st.button("Manage Courses"):
        st.session_state.admin_view = "ManageCourses"
    if st.button("Manage Users"):
        st.session_state.admin_view = "ManageUsers"
    if st.button("View Reports"):
        st.session_state.admin_view = "Reports"
    if st.button("↩"):
        st.session_state.admin_view = "Home"

view = st.session_state.admin_view

if view == "ManageCourses":
    ManageCourses.render()
elif view == "ManageUsers":
    ManageUsers.render()