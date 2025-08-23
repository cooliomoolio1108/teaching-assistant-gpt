import streamlit as st
from utils.auth import decode_jwt, bootstrap_and_persist
from utils.admin_functions import get_user
from utils.styling import inject_custom_css
from dotenv import load_dotenv
from utils.debug import debug_session_state
import st_cookie

inject_custom_css()
st.set_page_config(page_title="Home", layout="wide")
bootstrap_and_persist()
load_dotenv()

@st.dialog("⚠ Login Required")
def show_login_warning():
    st.write("You are about to log in via NTU SSO. Continue?")
    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("✅ Yes, log me in"):
            # Redirect to backend SSO
            st.markdown(
                f"<meta http-equiv='refresh' content='0; url={BACKEND_BASE}'>",
                unsafe_allow_html=True
            )

    with col2:
        if st.button("❌ Cancel"):
            st.rerun()
BACKEND_BASE = "http://localhost:5000/login"
if st.session_state.get("logged_in"):
    oid = st.session_state['user']['oid'] or ''
    user = get_user(oid)
    st.session_state['user']['role'] = user['role'] or 'nil'
    st.markdown(
        f"# Welcome, <span style='color:green'>{st.session_state["user"]['name']}</span>",
        unsafe_allow_html=True
    )
else:
    st.spinner("Checking Login Status")
    if st.button("Login via NTU SSO"):
        show_login_warning()
    st.spinner("Checking Login Status")

st_cookie.apply()

st.checkbox(
    "enabled",
    key="my_checkbox",
    on_change=lambda: st_cookie.update("login_token"),
)

debug_session_state()