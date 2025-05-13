from langchain_core.language_models.chat_models import BaseChatModel
from ..graphStates import AgentState
from ..utils import setup_logger

log = setup_logger(__name__)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You talk like a pirate. Answer all questions to the best of your ability. Your Name is {agentName}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def chat_agent_node(state: AgentState, llm_client: BaseChatModel):
    """
    Simple chatbot node that generates a response using the provided LLM client.

    Args:
        state: The current state of the graph, containing the message history.
               Expected format for state['messages']: List[Dict[str, Any]]
        llm_client: An instance of a language model client (e.g., GeminiClient).

    Returns:
        A dictionary containing the updated messages list.
    """
    # Extract messages from the state
    messages = state.get("messages")
    if not messages:
        log.warning("No messages found in the state at ChatAgentNode.")
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "No messages to process in graph's state at ChatAgentNode.",
                }
            ]
        }

    # Generate a response using the LLM client
    prompt = prompt_template.invoke(state)
    response = llm_client.invoke(prompt)
    log.debug(f"Response from LLM client at ChatAgentNode: {response}")

    # Return the updated messages list with the generated response
    return {"messages": [response], "randomBullshit": "test"}
