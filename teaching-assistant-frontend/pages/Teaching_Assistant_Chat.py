import streamlit as st
import requests
from utils.chat_functions import save_convo_id, save_message_to_db, get_convo_id, get_messages, send_to_gpt, simulate_streaming_from_response, feedback_in_chat, generate_title
from utils.admin_functions import get_all_courses
from utils.styling import inject_custom_css
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/conversation"
inject_custom_css()
st.set_page_config(page_title="Chat Panel", layout="wide")

if "courses" not in st.session_state:
    try:
        data = get_all_courses()
        st.session_state.courses = data
    except Exception as e:
        st.session_state.courses = []
        st.error(e)
    

@st.dialog("Creating Conversation")
def create_convo():
    options = st.session_state.courses
    if options and isinstance(options, (list, set, tuple)):
        course_options = {
            f"{option['course_name']}": option['id']  # Display title, store code
            for option in options
        }
        option = st.selectbox(
            "Choose a course for this conversation",
            course_options.keys(),
        )
        if option and st.button("submit", type="primary"):
            st.session_state.create_new_convo = True
            title = "New Chat"
            new_convo_id = save_convo_id(title, "user", course_options[option])
            if new_convo_id:
                st.session_state.conversations[new_convo_id] = {
                    "title": title,
                    "messages": [],
                    "title_updated": False
                }
                st.session_state.current_conversation = new_convo_id
            st.rerun()


if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

if "create_new_convo" not in st.session_state:
    st.session_state.create_new_convo = False

# Initialize session state
if "conversations" not in st.session_state:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        conversations = response.json()
        # Store as a dictionary: {title: []}
        st.session_state.conversations = {
            convo["_id"]: {
                "title": convo["title"],
                "messages": [],
                "title_updated": convo["title"] != "New Chat",
                "course_id": convo.get('course_code', '')
            }
            for convo in conversations
        }
    except Exception as e:
        st.session_state.conversations = {}
        st.error(f"Failed to load conversations: {str(e)}")
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = {}

# App Title
if st.session_state.current_conversation is None:
    st.title("Teacher Bot")
    st.subheader("Access all your conversations in the sidebar")

# Sidebar: Manage Conversations
with st.sidebar:
    st.header("Conversations")

    if st.button("New Conversation", type="primary"):
        create_convo()
        # st.session_state.create_new_convo = True
        # title = "New Chat"
        # new_convo_id = save_convo_id(title, "user")
        # if new_convo_id:
        #     st.session_state.conversations[new_convo_id] = {
        #         "title": title,
        #         "messages": [],
        #         "title_updated": False
        #     }
        #     st.session_state.current_conversation = new_convo_id


    for convo_id, convo_data in st.session_state.conversations.items():
        label = convo_data.get("title", "Untitled")
        if st.button(label, key=convo_id):
            st.session_state.current_conversation = convo_id


# Main Chat Window
if st.session_state.current_conversation:
    convo_id = st.session_state.current_conversation

    # Load message history from backend
    messages = get_messages(convo_id)
    st.session_state.conversations[convo_id]["messages"] = messages
    convo_data = st.session_state.conversations[convo_id]

    # Display conversation title
    st.write(f"# 🧠 {convo_data.get('title', 'Untitled Conversation')}")

    # Display message history
    # Inside main chat display loop
    for idx, msg in enumerate(messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# # Display feedback button only for the last assistant message
# if messages and messages[-1]["role"] == "assistant":
#     if st.button("👍", key=f"thumbs_up_last"):
#         feedback_in_chat(5)
#         st.success("Thank you for your feedback!")


    # Chat input
    prompt = st.chat_input("Say something...")

    if prompt:
            # Append user message to session + backend
        user_msg = {"role": "user", "content": prompt}
        convo_data["messages"].append(user_msg)
        save_message_to_db(convo_id, "user", prompt)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # TODO: Add GPT response handler here (send to backend, display, and save)
        with st.spinner("Thinking..."):            
            reply = send_to_gpt(convo_id)

        with st.chat_message("assistant"):
                st.write_stream(simulate_streaming_from_response('',reply))

        # if not st.session_state.feedback_given:
        #     if messages and messages[-1]["role"] == "assistant":
        #         if st.button("👍", key=f"thumbs_up_last"):
        #             st.session_state.feedback_given = True
        #             feedback_in_chat(5)
        assistant_msg = {"role": "assistant", "content": reply}
        st.session_state.conversations[convo_id]["messages"].append(assistant_msg)
        if (st.session_state.conversations[convo_id]["title"] == "New Chat"
            and len(st.session_state.conversations[convo_id]["messages"]) >= 4
            and not st.session_state.conversations[convo_id].get("title_updated", False)):
                new_title = generate_title(convo_id)
                if new_title:
                    st.session_state.conversations[convo_id]["title"] = new_title['title']
                    st.session_state.conversations[convo_id]["title_updated"] = True
        
else:
    st.warning("Please start a new conversation or access you past conversations in the sidebar.")