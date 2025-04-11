from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import chatbot

def build_graph() -> StateGraph:
    """ 
    Builds and returns the LangGraph workflow.
    Returns:
        The compiled StateGraph workflow.
    """
    workflow = StateGraph(AgentState)

    # Add nodes to the workflow
    workflow.add_node('chatbot', chatbot)

    # Define the edges (flow)
    workflow.add_edge(START, 'chatbot')
    workflow.add_edge('chatbot', END)

    # Compile and return the graph
    return workflow.compile()

# Build the graph instance when this module is imported
graph_instance = build_graph()
