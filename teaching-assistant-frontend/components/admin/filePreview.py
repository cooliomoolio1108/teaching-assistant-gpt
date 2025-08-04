import streamlit as st
import requests
from datetime import datetime
from urllib.parse import urlparse
from email.utils import parsedate_to_datetime

def render_file_card(file):
    dt = parsedate_to_datetime(file["uploaded_at"])
    
    st.markdown(f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
        background-color: rgb(14, 17, 23);
        transition: box-shadow 0.3s ease;
        height: 100%;
        display: flex;
    ">
        <h4 style="margin-top: 0; margin-bottom: 8px;">📄 {file['file_name']}</h4>
        <p style="margin: 0 0 6px 0;"<strong>{dt.strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
        <p style="margin: 0;">Embedded: <strong>{'Yes' if file['embedded'] else 'No'}</strong></p>
    </div>
    """, unsafe_allow_html=True)