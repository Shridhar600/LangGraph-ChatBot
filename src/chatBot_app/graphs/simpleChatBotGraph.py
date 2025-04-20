from ..graphStates import AgentState
from langgraph.graph import StateGraph, START, END
from ..nodes import chat_agent_node
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from ..utils import setup_logger

log = setup_logger(__name__)

def create_simple_graph(chatModel: BaseChatModel, memory, tools: list) -> CompiledStateGraph:
    
    tools_node = ToolNode(tools)
  
    workflow = StateGraph(AgentState) #Need to think about state, configurable or each graph has its own state.
    workflow.add_node('chatAgent', lambda state: chat_agent_node(state, chatModel)) #Used Lambda here because we need to pass a function to the node. This function will be called when the node is executed. It will pass the state to the Chat_agent_node.
    workflow.add_node("tools", tools_node) 
    workflow.add_edge(START, 'chatAgent')
    workflow.add_conditional_edges("chatAgent", tools_condition) # The tools_condition funct. exposes two edges for the Simple_chatbot Node 1. tools 2. END.
    workflow.add_edge('tools', 'chatAgent')
    graph = workflow.compile(checkpointer=memory,debug=False)
    log.info("Simple Graph compiled successfully.")
    return graph
