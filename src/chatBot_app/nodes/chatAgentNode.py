from langchain_core.language_models.chat_models import BaseChatModel
from ..graphStates import AgentState
from ..utils import setup_logger
from langchain_core.messages import SystemMessage
from ..utils import CHATBOT_SYSTEM_PROMPT, create_prompt_template

log = setup_logger(__name__)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def chat_agent_node(state: AgentState, llm_client: BaseChatModel, system_prompt: str = CHATBOT_SYSTEM_PROMPT) -> dict:
    """
    Simple chatbot node that generates a response using the provided LLM client.

    Args:
        state: The current state of the graph, containing the message history.
               Expected format for state['messages']: List[Dict[str, Any]]
        llm_client: An instance of a language model client (e.g., GeminiClient).
        system_prompt: The system prompt to use in the template. Defaults to CHATBOT_SYSTEM_PROMPT.

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
    
    prompt_template = create_prompt_template(system_prompt)
    prompt = prompt_template.invoke(state) # if you see here state is dictionary {"messages": "sadad", "agentName": "something passed here"}. 
    #Now, when we invoke the promptTemplate using state as a param we are basically pushing the variables messages and agentName inside the prompt. 
    # so messages contains the list of all messages in the state of the graph and agentName gets inserted at the system message. 
    response = llm_client.invoke(prompt)
    log.debug(f"Response from LLM client at ChatAgentNode: {response}")

    # Return the updated messages list with the generated response
    return {"messages": [response]}
