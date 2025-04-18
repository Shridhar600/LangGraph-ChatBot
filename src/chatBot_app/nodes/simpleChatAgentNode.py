from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from graphStates import AgentState


def simple_chatbot_node(state: AgentState, llm_client: BaseChatModel ):
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
    messages = state.get('messages')
    if not messages:
        return {"messages": [{"role": "assistant", "content": "No messages to process in graph's state at simple_chatbot_node."}]}
    
    # Generate a response using the LLM client
    response = llm_client.invoke(messages)
    # logger.debug(f"Generated response: {response}")
    
    # Return the updated messages list with the generated response
    return {"messages": messages + [{"role": "assistant", "content": response}]}