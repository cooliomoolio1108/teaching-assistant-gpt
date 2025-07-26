import streamlit as st
import threading
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
MSG_API_URL = os.getenv("FLASK_API_URL") + "/message"
CONVO_API_URL = os.getenv("FLASK_API_URL") + "/conversation"
GPT_API_URL = os.getenv("FLASK_API_URL") + "/chat"
FDBK_API_URL = os.getenv("FLASK_API_URL") + "/feedback"
TITLE_API_URL = os.getenv("FLASK_API_URL") + "/generate_title"
USER_API_URL = os.getenv("FLASK_API_URL") + "/users"

def get_all_users():
    try:
        response = requests.get(USER_API_URL)
        response.raise_for_status()  # raises HTTPError if status != 2xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"❌ Request failed: {req_err}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")