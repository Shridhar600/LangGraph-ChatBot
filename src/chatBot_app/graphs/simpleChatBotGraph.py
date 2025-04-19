from chatBot_app.graphStates import AgentState
from langgraph.graph import StateGraph, START, END
from chatBot_app.nodes import chat_agent_node
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph

def create_simple_graph(chatModel: BaseChatModel, memory) -> CompiledStateGraph:
    workflow = StateGraph(AgentState) #Need to think about state, configurable or each graph has its own state.
    
    workflow.add_node('simple_chatbot', lambda state: chat_agent_node(state, chatModel)) #Used Lambda here because we need to pass a function to the node. This function will be called when the node is executed. It will pass the state to the Chat_agent_node.
    workflow.add_edge(START, 'simple_chatbot')
    workflow.add_edge('simple_chatbot', END)
    graph =  workflow.compile(checkpointer=memory)
    print("Simple Graph compiled successfully.")
    return graph
