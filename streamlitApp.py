import streamlit as st
import uuid
from src.chatBot_app import (
    ChatBot, get_tools, tools, CHATBOT_SYSTEM_PROMPT, # tools is imported here but also defined by load_tools later
    create_llm_client, create_simple_graph,
    get_in_memory_store, setup_logger
)
from src.chatBot_app.utils.exceptions import (
    LLMAPIError, ToolExecutionError, GraphError, AppException,
    LLMInitializationError, ToolInitializationError, ConfigurationError,
    InvalidStateError, EmbeddingError, VectorStoreError, DocumentLoadingError
)
# ConfigurationError is also in src.chatBot_app.config, but utils.exceptions.ConfigurationError should be sufficient as it's the base for others or a direct import.
# If src.chatBot_app.config.ConfigurationError is a different, more specific one, that might need aliasing. Assuming they are compatible or utils.exceptions.ConfigurationError is the one to use.

from src.rag_app.core.vector_store_singleton import VECTOR_STORE  # Ensure vector store is initialized at startup

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
def load_tools_cached(): # Renamed to avoid conflict with imported tools
    log.info("Creating tools...")
    try:
        return get_tools()
    except ToolInitializationError as e:
        log.critical(f"Failed to load essential tools: {e}", exc_info=True)
        st.error(f"CRITICAL ERROR: Failed to load essential tools: {e}. Application might be unstable.")
        # Depending on criticality, could st.stop() here.
        # For now, allow app to continue with potentially missing tools, or tools that don't init.
        return [] # Return empty list or handle appropriately

@st.cache_resource
def load_llm_client_cached(_tools: list, _is_tool_enabled: bool): # Renamed
    log.info("Initializing LLM Client...")
    try:
        return create_llm_client(_tools, _is_tool_enabled)
    except LLMInitializationError as e:
        log.critical(f"Failed to initialize LLM client: {e}", exc_info=True)
        st.error(f"CRITICAL ERROR: Failed to initialize LLM client: {e}. Application cannot continue.")
        st.stop()

@st.cache_resource
def load_memory_store_cached(): # Renamed
    log.info("Initializing Memory Store...")
    # Assuming get_in_memory_store() is robust or doesn't throw custom exceptions handled here
    return get_in_memory_store()

@st.cache_resource
def load_graph_cached(_chat_model, _memory, _tools): # Renamed
    log.info("Compiling Graph...")
    try:
        return create_simple_graph(_chat_model, _memory, _tools, CHATBOT_SYSTEM_PROMPT)
    except GraphError as e: # Or InvalidStateError depending on create_simple_graph's behavior
        log.critical(f"Failed to create chat graph: {e}", exc_info=True)
        st.error(f"CRITICAL ERROR: Failed to create chat graph: {e}. Application cannot continue.")
        st.stop()
    except InvalidStateError as e: # If graph creation itself has state issues
        log.critical(f"Failed to create chat graph due to invalid state: {e}", exc_info=True)
        st.error(f"CRITICAL ERROR: Failed to create chat graph due to invalid state: {e}. Application cannot continue.")
        st.stop()


@st.cache_resource
def load_chatbot_cached(_graph): # Renamed
    log.info("Initializing ChatBot...")
    try:
        return ChatBot(_graph)
    except InvalidStateError as e:
        log.critical(f"Failed to initialize ChatBot: {e}", exc_info=True)
        st.error(f"CRITICAL ERROR: Failed to initialize ChatBot: {e}. Application cannot continue.")
        st.stop()

# --- Global Resource Loading with Error Handling ---
# This block attempts to load all critical resources.
# VECTOR_STORE is imported above, its initialization (rag_setup) happens at import time.
# So, we wrap this entire section.
try:
    # Attempt to access VECTOR_STORE to trigger its initialization if not already done,
    # or to confirm it's available after import. This line is more of a placeholder
    # to ensure this try-block is relevant for VECTOR_STORE related errors from its singleton import.
    # Actual errors from rag_setup (if it runs on import of VECTOR_STORE) would have occurred before this line.
    # The import line itself for VECTOR_STORE might be where the error originates.
    # For robustness, we assume rag_setup might be triggered by the import of VECTOR_STORE.
    # If rag_setup can fail, the app should not proceed.
    # The challenge is catching errors from an import statement directly if it's not a ModuleNotFoundError.
    # We'll assume that if VECTOR_STORE import was problematic and led to an unhandled exception,
    # Streamlit might not even start this script properly.
    # The following loads are more explicit and can be caught here.

    loaded_tools = load_tools_cached() # Renamed variable to avoid conflict
    chat_model = load_llm_client_cached(loaded_tools, enable_tools)
    memory = load_memory_store_cached()
    # Pass loaded_tools instead of the imported 'tools' which might be a module
    graph = load_graph_cached(chat_model, memory, loaded_tools) 
    chatbot = load_chatbot_cached(graph)

except (DocumentLoadingError, EmbeddingError, VectorStoreError, ConfigurationError) as e:
    # These are relevant for RAG/VECTOR_STORE initialization.
    # ConfigurationError can also come from AppSettings if LLM keys etc. are missing for RAG.
    log.critical(f"Fatal error during RAG system or critical configuration: {e}", exc_info=True)
    st.error(f"CRITICAL ERROR: Failed to initialize RAG system or critical configuration: {e}. Application cannot start.")
    st.stop()
except LLMInitializationError as e: # Catch if load_llm_client_cached was not called yet or error bubbled up
    log.critical(f"LLM Initialization Error before chat interaction: {e}", exc_info=True)
    st.error(f"CRITICAL ERROR: LLM could not be initialized: {e}. Application cannot start.")
    st.stop()
except ToolInitializationError as e: # Catch if load_tools_cached was not called yet or error bubbled up
    log.critical(f"Tool Initialization Error before chat interaction: {e}", exc_info=True)
    st.error(f"CRITICAL ERROR: Tools could not be initialized: {e}. Application may be unstable.")
    # Not stopping, as some tools might be optional or app could run without them.
except GraphError as e: # Catch if load_graph_cached was not called yet or error bubbled up
    log.critical(f"Graph Error before chat interaction: {e}", exc_info=True)
    st.error(f"CRITICAL ERROR: Graph could not be initialized: {e}. Application cannot start.")
    st.stop()
except InvalidStateError as e: # Catch if load_chatbot_cached was not called yet or error bubbled up
    log.critical(f"Invalid State Error before chat interaction: {e}", exc_info=True)
    st.error(f"CRITICAL ERROR: Core component in invalid state: {e}. Application cannot start.")
    st.stop()
except Exception as e: # Catch any other unexpected error during setup
    log.critical(f"An unexpected critical error occurred during application setup: {e}", exc_info=True)
    st.error(f"CRITICAL UNEXPECTED ERROR: {e}. Application cannot start.")
    st.stop()

# --- Chat History Display ---

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
                # Correctly iterate over the stream if it's a list of chunks (as per current ChatBot.stream_graph)
                # If stream_graph itself is a generator, this loop is fine.
                # Based on ChatBot.stream_graph, it returns a list, so this should be fine.
                for chunk in response_stream: # Assuming response_stream is a list of content strings
                    if isinstance(chunk, str):
                        assistant_reply += chunk
                    # If stream_graph yields dicts or other objects, this needs adjustment:
                    # e.g., if chunk is a dict with 'content': assistant_reply += chunk.get('content', '')
                    else:
                        # This case might indicate an unexpected item in the list from stream_graph
                        log.warning(f"Unsupported chunk type in response_stream: {type(chunk)}")
                        assistant_reply += "\n[Unsupported format in stream]"
                
                if not assistant_reply and response_stream: # If stream had non-string items that resulted in no text
                    if not assistant_reply: # Check if still empty
                        assistant_reply = "[No textual response generated or error in response structure]"

                st.markdown(assistant_reply)
                st.session_state.history.append(("assistant", assistant_reply))

            except LLMAPIError as e:
                error_msg = f"LLM API Error: {str(e)}"
                st.error(error_msg)
                log.exception("LLMAPIError during assistant response.")
            except ToolExecutionError as e:
                error_msg = f"Tool Execution Error: {str(e)}"
                st.error(error_msg)
                log.exception("ToolExecutionError during assistant response.")
            except GraphError as e:
                error_msg = f"Graph Execution Error: {str(e)}"
                st.error(error_msg)
                log.exception("GraphError during assistant response.")
            except InvalidStateError as e:
                error_msg = f"Invalid State Error: {str(e)}"
                st.error(error_msg)
                log.exception("InvalidStateError during assistant response.")
            except AppException as e: # Catch-all for other app-specific issues
                error_msg = f"Application Error: {str(e)}"
                st.error(error_msg)
                log.exception("AppException during assistant response.")
            except Exception as e: # General fallback
                error_msg = f"An unexpected error occurred: {str(e)}"
                st.error(error_msg)
                log.exception("Unexpected error during assistant response.")
