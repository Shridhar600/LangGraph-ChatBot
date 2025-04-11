from llmFactory import getLLMClient
from utils.logger import logger
from .state import AgentState
from agents.chat_agent import ChatAgent

# need to try dependency injection here
llm_client = getLLMClient().get_client()

chat_agent_instance = None

if llm_client:
    try:
        chat_agent_instance = ChatAgent(llm_client)
        logger.info("ChatAgent instance created successfully in graph/nodes.py")
    except TypeError as e:
        logger.error(f"Failed to initialize ChatAgent due to invalid LLM client: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred during ChatAgent initialization: {e}", exc_info=True)
else:
    logger.error("LLM client is None, cannot initialize ChatAgent.")

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
