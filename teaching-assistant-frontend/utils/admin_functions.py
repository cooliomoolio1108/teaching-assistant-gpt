import streamlit as st
import threading
import requests
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()
MSG_API_URL = os.getenv("FLASK_API_URL") + "/message"
CONVO_API_URL = os.getenv("FLASK_API_URL") + "/conversation"
GPT_API_URL = os.getenv("FLASK_API_URL") + "/chat"
FDBK_API_URL = os.getenv("FLASK_API_URL") + "/feedback"
TITLE_API_URL = os.getenv("FLASK_API_URL") + "/generate_title"
USER_API_URL = os.getenv("FLASK_API_URL") + "/users"
COURSE_API_URL = os.getenv("FLASK_API_URL") + "/courses"
FILE_API_URL = os.getenv("FLASK_API_URL") + "/files"
EMBED_API_URL = os.getenv("FLASK_API_URL") + "/embed"

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

def get_all_courses():
    try:
        response = requests.get(COURSE_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"❌ Request failed: {req_err}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

def get_course(id):
    try:
        url = COURSE_API_URL + f'/{id}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"❌ Request failed: {req_err}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

def get_files(course_id=None):
    try:
        if course_id:
            response = requests.get(FILE_API_URL, params={'course_id': course_id})
        else:
            response = requests.get(FILE_API_URL)

        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        try:
            error_detail = response.json().get("error", "Unknown error")
        except Exception:
            error_detail = response.text or "No error detail provided"
        st.error(f"❌ HTTP error {response.status_code}: {error_detail}")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the server. Is the backend running?")
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")



def is_safe_folder_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_\-]+", name))

def upload_files(data, files):
    # Validate inputs
    if not isinstance(data, dict):
        raise TypeError("Expected input data as a dictionary.")
    if not isinstance(files, dict):
        raise TypeError("Expected files to be passed as a dictionary.")

    required_keys = ["file_name", "path", "course_id", "uploaded_by", "file_size"]
    if not all(k in data for k in required_keys):
        raise ValueError(f"Missing one of the required fields: {required_keys}")

    try:
        # Prepare form data (metadata)
        form_data = {
            "file_name": data["file_name"],
            "path": data["path"],
            "course_id": data["course_id"],
            "uploaded_by": data["uploaded_by"],
            "file_size": str(data["file_size"]),  # must be string for form field
            "embedded": "False"
        }

        # Send both file and metadata together
        response = requests.post(FILE_API_URL, files=files, data=form_data)

        if response.status_code in (200, 201):
            return response.json().get("_id") or response.json().get("file_id")
        else:
            print(f"[ERROR] API returned {response.status_code}: {response.text}")
            return None

    except requests.RequestException as e:
        print(f"[ERROR] Failed to connect to backend: {e}")
        return None

def embed_files(file_ids):
    response = requests.post(EMBED_API_URL, json=file_ids)
    print("response.status_code", response.status_code)
    if response.status_code in (200, 201):
        return response.json().get("status")
    else:
        print(f"[ERROR] API returned {response.status_code}: {response.text}")
        return None