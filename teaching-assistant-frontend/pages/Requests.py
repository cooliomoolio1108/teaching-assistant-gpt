import streamlit as st
from components import sidebar_menu
from utils.auth import require_login
from dotenv import load_dotenv
from utils.styling import inject_custom_css
from components.dashboard_card import dashboard_card
from components import dashboard_cards_function as card

require_login()
load_dotenv()
st.set_page_config(page_title="Course Panel", layout="wide")
inject_custom_css()
sidebar_menu.authenticated_menu()

st.title("Requests")
dashboard_card("Register a Course", card.request_course)