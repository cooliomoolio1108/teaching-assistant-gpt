import streamlit as st
import jwt, time
import os
from dotenv import load_dotenv
from streamlit_cookies_manager import CookieManager
from streamlit_cookies_controller import CookieController

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")  # must match your Flask's signing key

def decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        st.error("Session expired.")
    except jwt.InvalidTokenError:
        st.error("Invalid token.")
    return None

def create_jwt(payload: dict):
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def bootstrap_and_persist():
    # 1) If session empty but URL has token, decode + store
    if "login_token" in st.session_state:
        claims = decode_jwt(cookie)
        if claims:
            st.session_state["api_token"] = cookie
            st.session_state["user"] = claims
            st.session_state["logged_in"] = True 
    controller = CookieController()
    cookie = controller.get('login_token')
    # token = st.query_params.get("token")
    if cookie and "login_token" not in st.session_state:
        claims = decode_jwt(cookie)
        if claims:
            st.session_state["api_token"] = cookie
            st.session_state["user"] = claims
            st.session_state["logged_in"] = True
    # 2) Keep token in URL so refresh/page switch won’t lose it
    # if "api_token" in st.session_state and not st.query_params.get("token"):
    #     st.query_params["token"] = st.session_state["api_token"]

def require_login(login_url="http://localhost:5000/login"):
    bootstrap_and_persist()
    if not st.session_state.get("logged_in"):
        st.switch_page('Home.py')
    # defense-in-depth (domain)
    email = (st.session_state["user"].get("email") or "").lower()
    if not (email.endswith("@ntu.edu.sg") or email.endswith("@e.ntu.edu.sg")):
        st.error("Access denied: NTU only."); st.stop()