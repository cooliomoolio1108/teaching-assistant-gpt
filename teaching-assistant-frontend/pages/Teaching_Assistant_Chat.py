import streamlit as st
from openai import AzureOpenAI
# import os
# from dotenv import load_dotenv
# from azure.identity import DefaultAzureCredential, get_bearer_token_provider
# from langchain_openai import AzureChatOpenAI

# load_dotenv()
# llm_stream = AzureChatOpenAI(
#     azure_endpoint=os.getenv("AZ_OPENAI_ENDPOINT"),
#     openai_api_version="2024-05-01-preview",
#     model_name="gpt-35-turbo",
#     openai_api_key=os.getenv("AZ_OPENAI_API_KEY"),
#     openai_api_type="azure",
#     temperature=0.3,
#     streaming=True,
# )
# prompt = "Tell me something about Azure"

# for chunk in llm_stream.stream(prompt):
#     print(chunk.content, end="", flush=True)
st.title("Teacher Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Teacher: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})