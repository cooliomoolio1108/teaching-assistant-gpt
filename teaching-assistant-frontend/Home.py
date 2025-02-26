import streamlit as st
from components.module_card import show_card
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/status"
response = requests.get(API_URL)

with open("assets/Machine-Learning.jpg", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
data = "data:image/png;base64," + encoded.decode("utf-8")

st.title("Home Page")

with st.container():
    st.subheader("Your Courses")
    show_card(data, "SC4172", "This course is about...", "card1")
    show_card("dasdsa", "SC3000", "This Course is about...", "card2")
