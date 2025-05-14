import streamlit as st
import uuid
from src.chatBot_app import (
    ChatBot, get_tools, tools, CHATBOT_SYSTEM_PROMPT,
    create_llm_client, create_simple_graph,
    get_in_memory_store, setup_logger
)

log = setup_logger(__name__)

import hashlib

# --- Page Config ---
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")

# --- User Authentication ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Predefined users (username: hashed_password)
USERS = {
    "admin": hash_password("admin123"),
    "demo": hash_password("demo123"),
}

def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in USERS and hash_password(password) == USERS[username]:
            st.session_state.logged_in = True
            st.session_state.username = username
            # Create a user-specific thread ID
            st.session_state.thread_id = f"{st.session_state.username}_{uuid.uuid4().hex[:8]}"
            st.session_state.username_for_thread = st.session_state.username
            if hasattr(st, "rerun"):
                st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.history = []
        st.session_state.thread_id = None
        if hasattr(st, "rerun"):
            st.rerun()

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Login flow
if not st.session_state.logged_in:
    login()
    st.stop()  # Stop the app until login is successful
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    logout()

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# --- Sidebar: Settings ---
st.sidebar.title("⚙️ Settings")
enable_tools = st.sidebar.toggle("Enable Tools", value=True)
theme_toggle = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
st.session_state.theme = theme_toggle

# --- Dynamic Styling ---
light_theme = """
    <style>
        .block-container {
            padding: 2rem 2rem;
        }
        .stChatMessage {
            background-color: #f0f2f6;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
"""

dark_theme = """
    <style>
        .block-container {
            padding: 2rem 2rem;
        }
        .stChatMessage {
            background-color: #2e2e2e;
            color: #f0f0f0;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
"""

st.markdown(light_theme if st.session_state.theme == "Light" else dark_theme, unsafe_allow_html=True)

# --- Header ---
st.title("🧠 LangGraph Chatbot")
st.caption(f"Thread ID: `{st.session_state.thread_id}`")

# --- Load Resources ---
@st.cache_resource
def load_tools():
    log.info("Creating tools...")
    return get_tools()

@st.cache_resource
def load_llm_client(_tools: list, _is_tool_enabled: bool):
    log.info("Initializing LLM Client...")
    return create_llm_client(_tools, _is_tool_enabled)

@st.cache_resource
def load_memory_store():
    log.info("Initializing Memory Store...")
    return get_in_memory_store()

@st.cache_resource
def load_graph(_chat_model, _memory, _tools):
    log.info("Compiling Graph...")
    return create_simple_graph(_chat_model, _memory, _tools, CHATBOT_SYSTEM_PROMPT)

@st.cache_resource
def load_chatbot(_graph):
    log.info("Initializing ChatBot...")
    return ChatBot(_graph)

tools = load_tools()
chat_model = load_llm_client(tools, enable_tools)
memory = load_memory_store()
graph = load_graph(chat_model, memory, tools)
chatbot = load_chatbot(graph)

# --- Chat History Display ---
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)

# --- User Input ---
if prompt := st.chat_input("Type your message..."):
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_stream = chatbot.stream_graph(prompt, st.session_state.thread_id)
                assistant_reply = ""
                for chunk in response_stream:
                    if isinstance(chunk, str):
                        assistant_reply += chunk
                    else:
                        assistant_reply += "\n[Unsupported format]"
                st.markdown(assistant_reply)
                st.session_state.history.append(("assistant", assistant_reply))
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.error(error_msg)
                log.exception("Error during assistant response.")
