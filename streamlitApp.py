import random
import streamlit as st
from graph.workflow import graph_instance
from interfaces.streamlit import stream_graph_and_get_response
from userInfo.userConfig import userSessionID

st.title("🧠 LangGraph Chatbot (Web Interface)")
st.markdown("Ask your AI anything:")

#Create a thread id 
config = {"configurable": {"thread_id": userSessionID}} # This is a random number to identify the thread

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("User:", "")

if user_input:
    # Call the LangChain graph
    assistant_reply = stream_graph_and_get_response(graph_instance, user_input, config)

    # Store in chat history
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("assistant", assistant_reply))

# Show chat history
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)
