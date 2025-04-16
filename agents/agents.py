from agents.chat_agent import ChatAgent
from agents.chat_agent_with_tools import ChatAgentWithTools
from llm_clients.llmFactory import getLLMClient





def getChatAgentWithTools() -> ChatAgentWithTools:
    """
    Factory function to get an instance of the ChatAgentWithTools class.
    
    Returns:
        An instance of ChatAgentWithTools, or None if the LLM client is not available.
    """
    llm_client_wrapper = getLLMClient() 
    llm_client = llm_client_wrapper.get_client() if llm_client_wrapper else None 
    
    if llm_client is None:
        raise ValueError("LLM client is not available. Cannot create ChatAgentWithTools instance.")
    
    from tools.tools import getToolsForLLM
    tools = getToolsForLLM() 
    
    chat_agent = ChatAgentWithTools(llm_client, tools) 
    
    return chat_agent


def getChatAgent() -> ChatAgent:
    """
    Factory function to get an instance of the ChatAgent class.
    
    Returns:
        An instance of ChatAgentWithTools, or None if the LLM client is not available.
    """
    llm_client_wrapper = getLLMClient() 
    llm_client = llm_client_wrapper.get_client() if llm_client_wrapper else None 

    if llm_client is None:
        raise ValueError("LLM client is not available. Cannot create ChatAgent instance.")
    
    chat_agent = ChatAgent(llm_client) 
    
    return chat_agent