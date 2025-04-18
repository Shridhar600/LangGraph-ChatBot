from graph.state import AgentState
from langgraph.graph import StateGraph, START, END
from nodes import simple_chatbot_node
from langchain_core.language_models.chat_models import BaseChatModel


def create_simple_graph(chatModel: BaseChatModel) -> StateGraph:
    workflow = StateGraph(AgentState)
    
    workflow.add_node('simple_chatbot', lambda state: simple_chatbot_node(state, chatModel))
    workflow.add_edge(START, 'simple_chatbot')
    workflow.add_edge('simple_chatbot', END)
    graph =  workflow.compile()
    print("Graph compiled successfully.")
    return graph