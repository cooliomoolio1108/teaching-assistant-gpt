import streamlit as st
import requests
from utils.chat_functions import save_convo_id, save_message_to_db, get_convo_id, get_messages, send_to_gpt, simulate_streaming_from_response, feedback_in_chat, generate_title
from utils.styling import inject_custom_css
from dotenv import load_dotenv
import os
import pyperclip
import time

load_dotenv()
API_URL = os.getenv("FLASK_API_URL") + "/conversation"
inject_custom_css()

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Initialize session state
if "conversations" not in st.session_state:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        conversations = response.json()
        print("CONVERSATIONS: ", conversations)
        # Store as a dictionary: {title: []}
        st.session_state.conversations = {
            convo["_id"]: {
                "title": convo["title"],
                "messages": [],
                "title_updated": convo["title"] != "New Chat" 
            }
            for convo in conversations
        }
        print("HERE",st.session_state.conversations)
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
        title = "New Chat"
        new_convo_id = save_convo_id(title, "user")
        if new_convo_id:
            st.session_state.conversations[new_convo_id] = {
                "title": title,
                "messages": [],
                "title_updated": False
            }
            st.session_state.current_conversation = new_convo_id


    for convo_id, convo_data in st.session_state.conversations.items():
        label = convo_data.get("title", "Untitled")
        if st.button(label, key=convo_id):
            st.session_state.current_conversation = convo_id


# Main Chat Window
if st.session_state.current_conversation:
    convo_id = st.session_state.current_conversation
    print(f"Active conversation: {convo_id}")

    # Load message history from backend
    messages = get_messages(convo_id)
    st.session_state.conversations[convo_id]["messages"] = messages
    convo_data = st.session_state.conversations[convo_id]
    print(convo_data)

    # Display conversation title
    st.write(f"### 🧠 {convo_data.get('title', 'Untitled Conversation')}")

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
            and len(st.session_state.conversations[convo_id]["messages"]) >= 2
            and not st.session_state.conversations[convo_id].get("title_updated", False)):
                new_title = generate_title(convo_id)
                print("THE NEW TITLE IS ", new_title)
                if new_title:
                    st.session_state.conversations[convo_id]["title"] = new_title['title']
                    print("SEARCG+H", st.session_state.conversations[convo_id]["title"])
                    st.session_state.conversations[convo_id]["title_updated"] = True
        
else:
    st.warning("Please start a new conversation or access you past conversations in the sidebar.")