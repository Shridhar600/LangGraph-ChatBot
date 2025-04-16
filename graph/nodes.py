from agents.agents import getChatAgentWithTools
from llm_clients.llmFactory import getLLMClient
from tools.tools import getToolsForLLM
from utils.logger import logger
from .state import AgentState
from langgraph.prebuilt import ToolNode


# --- Graph Node ---
def chatbot(state: AgentState) -> dict:
    """ 
    Graph node that invokes the ChatAgent to generate a response.

    Args:
        state: The current state of the graph, containing the message history. 
               Expected format for state['messages']: List[Dict[str, Any]]

    Returns:
        A dictionary containing the updated messages list, typically with the agent's response.
        Returns an error message if the agent is not initialized.
    """
    chat_agent_instance = getChatAgentWithTools()

    if chat_agent_instance is None:
        logger.error("ChatAgent instance is not available in chatbot node.")
        return {"messages": [{"role": "assistant", "content": "Sorry, the chatbot agent is not initialized correctly."}]}

    # Extract messages from the state
    messages = state.get('messages')
    if not messages:
        logger.warning("Chatbot node received state with no messages.")
        pass # Let the agent handle the empty list

    # logger.debug(f"Passing messages to ChatAgent: {messages}")

    return chat_agent_instance.generate_response(messages)


# make another node for chatbotWithTools later.

def getToolsNode() -> ToolNode: 
    tools = getToolsForLLM() # Get the list of tools for the LLM client
    return ToolNode(tools=tools) # Create a ToolNode with the tools