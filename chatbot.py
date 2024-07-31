import os
import streamlit as st
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from query_vector_store import query_vector_index

# Set your OpenAI API key
if "OPENAI_API_KEY" in st.secrets:
    my_api_key = st.secrets["OPENAI_API_KEY"]
else:
    my_api_key = st.sidebar.text_input(
        label = "#### Set your OpenAI API key here 👇",
        placeholder = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type = "password")

# Set your data directory path
if "DATA_DIRECTORY_PATH" in st.secrets:
    my_directory_path = st.secrets["DATA_DIRECTORY_PATH"]
else:
    my_directory_path = st.sidebar.text_input(
        label = "#### Set your data directory path here 👇",
        placeholder = "C:\\path\\to\\your\\data\\directory",
        type = "default")


# Sidebar for user details
st.sidebar.title("User Verification")
user_name = st.sidebar.text_input("Name")
account_number = st.sidebar.text_input("Account Number")
verify_button = st.sidebar.button("Verify")

if verify_button:
    if user_name and account_number:
        st.sidebar.success(f"User {user_name} with account {account_number} verified.")
    else:
        st.sidebar.error("Please enter both name and account number.")


# App title
st.title("OTC HS Chatbot")

# Set OpenAI model to the Streamlit session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Set messages to the Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Iterate over the messages in the Streamlit session state and display them
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add user input and response to the Streamlit session state
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the conversation history to be sent to the LLM
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    # Set up the LlamaOpenAI model with specified settings
    Settings.llm = LlamaOpenAI(
        system_prompt = "You are a helpful customer assistant tasked with helping customer understand about OTC HS program and products they can buy at CVS. \
        When asked a question, answer from the data directory. \
            If you don't know the answer, say 'Oh, snap! It seems I've hit a road bump in my knowledge highway, \
            maybe I can try and help you connect with a live agent'. \
            If you know the answer, please provide trip information not in a list but in text.",
        model = st.session_state["openai_model"],
        openai_api_key = my_api_key,
        max_tokens = 250
    )

    with st.chat_message("assistant"):
        full_prompt = f"{conversation_history}\n user: {prompt}"
        streaming_response = query_vector_index(full_prompt)
        streaming_response = query_vector_index(prompt)
        print("@@@@@@@@@", type(streaming_response))
        print(streaming_response)

        response = st.write(streaming_response.response)
    st.session_state.messages.append({"role": "assistant", "content": streaming_response.response})
