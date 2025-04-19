import streamlit as st
from src.chatBot_app import ChatBot
from src.chatBot_app import create_llm_client
from src.chatBot_app import create_simple_graph
from src.chatBot_app import getInMemoryStore

st.title("🧠 LangGraph Chatbot (Web Interface)")
st.markdown("Ask your AI anything:")

# project_root = os.path.abspath(os.path.dirname(__file__))
# src_path = os.path.join(project_root, "src")
# if src_path not in sys.path:
#     sys.path.insert(0, os.path.abspath(src_path))

chatModel = create_llm_client()
memory = getInMemoryStore()
graph = create_simple_graph(chatModel,memory)
chatbot = ChatBot(graph) 
print("objects initialized")

if "history" not in st.session_state:
    st.session_state.history = []

current_thread_id = f"cli_thread_1"

user_input = st.text_input("User:", "")

if user_input:
    # Call the LangChain graph
    assistant_reply = chatbot.stream_graph(user_input, current_thread_id)

    # Store in chat history
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("assistant", assistant_reply))

# Show chat history
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)
