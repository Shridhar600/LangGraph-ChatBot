import streamlit as st
from src.chatBot_app import ChatBot
from src.chatBot_app import create_llm_client
from src.chatBot_app import create_simple_graph
from src.chatBot_app import get_in_memory_store
from src.chatBot_app import setup_logger

log = setup_logger(__name__)


# --- Cached Resource Creation Functions ---
@st.cache_resource
def load_llm_client():
    log.info("Initializing LLM Client...")  # This will print only once
    return create_llm_client()


@st.cache_resource
def load_memory_store():
    log.info("Initializing Memory Store...")  # This will print only once
    return get_in_memory_store()


@st.cache_resource
def load_graph(
    _chat_model, _memory
):  # Arguments starting with _ signal cache to ignore them
    log.info("Compiling Graph...")  # This will print only once
    return create_simple_graph(_chat_model, _memory)


@st.cache_resource
def load_chatbot(_graph):
    log.info("Initializing ChatBot...")  # This will print only once
    return ChatBot(_graph)


# --- Main App Logic ---
st.title("🧠 LangGraph Chatbot (Web Interface)")
st.markdown("Ask your AI anything:")

# Get cached objects
chatModel = load_llm_client()
memory = load_memory_store()
graph = load_graph(chatModel, memory)  # Pass objects needed for creation
chatbot = load_chatbot(graph)

# Initialize chat history in session state if it doesn't exist
if "history" not in st.session_state:
    st.session_state.history = []

# Use a fixed or session-specific thread ID (this part might need refinement later)
current_thread_id = "st_session_1"  # Simple example

user_input = st.text_input("User:", "")

if user_input:
    # Call the LangChain graph using the cached chatbot instance
    assistant_reply = chatbot.stream_graph(user_input, current_thread_id)

    # Store in chat history (session state handles this persistence)
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("assistant", assistant_reply))

# Show chat history
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)
