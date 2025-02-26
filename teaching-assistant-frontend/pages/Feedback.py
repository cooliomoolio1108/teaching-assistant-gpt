import streamlit as st
from streamlit_star_rating import st_star_rating
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/submit_feedback"

st.title("Feedback")

with st.form(
    key="feedback",
    clear_on_submit=True,
    enter_to_submit=True,
    border=True
):
    stars = st_star_rating("Please rate your experience", maxValue=5, defaultValue=0, key="rating")
    comment = st.text_area("Write your feedback:")

    submitted = st.form_submit_button("Submit")
    if submitted:
        response = requests.post(API_URL, json={
            "stars": stars,
            "comments": comment
        })
        st.warning("Thank you for submitting!")