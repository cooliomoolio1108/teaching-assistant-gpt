import streamlit as st
from components.module_card import show_card
import os
import requests
from dotenv import load_dotenv
import base64
from utils.styling import inject_custom_css

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/status"
response = requests.get(API_URL)

with open("assets/Machine-Learning.jpg", "rb") as f:
    data1 = f.read()
    encoded1 = base64.b64encode(data1)
data1 = "data:image/png;base64," + encoded1.decode("utf-8")

with open("assets/bgimg.jpg", "rb") as f:
    data2 = f.read()
    encoded2 = base64.b64encode(data2)
data2 = "data:image/png;base64," + encoded2.decode("utf-8")

st.logo("assets/chatbot.png", size="large")
inject_custom_css()
st.title("Home Page")
st.subheader("Your Courses")


col1, col2 = st.columns(2, gap="medium")
with col1:
    show_card(data1, "SC4172", "This course is about...", "card1")
with col2:
    show_card(data2, "SC3000", "This Course is about...", "card2")
