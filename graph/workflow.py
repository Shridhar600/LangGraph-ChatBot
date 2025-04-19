from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import chatbot,getToolsNode
from langgraph.prebuilt import tools_condition
from chatBot_app.memory.inMemoryStore import getInMemoryStore


def build_graph(memory) -> StateGraph:
    """ 
    Builds and returns the LangGraph workflow.
    Returns:
        The compiled StateGraph workflow.
    """
    toolNode = getToolsNode()
    workflow = StateGraph(AgentState)

    # Add nodes to the workflow
    workflow.add_node('chatbot', chatbot)
    workflow.add_node("tools", toolNode)
    # Define the edges (flow)
    workflow.add_edge(START, 'chatbot')
    workflow.add_conditional_edges("chatbot", tools_condition)
    workflow.add_edge('tools', 'chatbot')
    workflow.add_edge('chatbot', END)

    # Compile and return the graph
    return workflow.compile(checkpointer=memory)

# Build the graph instance when this module is imported
memory = getInMemoryStore()
graph_instance = build_graph(memory)
