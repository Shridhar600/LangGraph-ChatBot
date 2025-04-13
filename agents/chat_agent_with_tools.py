from typing import List, Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from utils.logger import logger

class ChatAgentWithTools:
    """
    Handles the core logic of interacting with the LLM and binding it with tools for chatbot responses.
    """
    def __init__(self, llm_client: BaseChatModel, tools: List):
        if not isinstance(llm_client, BaseChatModel):
             # Log and raise an error if the client is not a valid LangChain chat model
             logger.error(f"ChatAgentWithTools received an invalid LLM client type: {type(llm_client)}")
             raise TypeError("llm_client must be an instance of BaseChatModel or its subclass.")
        self.llm_client = llm_client.bind_tools(tools)
        logger.info(f"ChatAgentWithTools initialized with LLM client: {type(llm_client)}")

    def generate_response(self, messages: List[Dict[str, Any]]) -> Dict[str, List[BaseMessage]]:
        """
        Generates a response from the LLM based on the provided message history.

        Args:
            messages: A list of messages representing the conversation history. 
                      Expected format: [{"role": "user/assistant", "content": "..."}]

        Returns:
            A dictionary containing the 'messages' key with a list containing the LLM's response message.
            Handles errors gracefully by returning an error message.
        """
        if not messages:
            logger.warning("ChatAgentWithTools generate_response called with empty messages.")
            # Return a default response or indicate an issue
            return {"messages": [{"role": "assistant", "content": "It looks like the conversation history is empty. How can I help?"}]}

        try:
            logger.info(f"ChatAgentWithTools invoking LLM with messages: {messages}")
            response = self.llm_client.invoke(messages) 
            logger.info(f"ChatAgentWithTools received LLM response: {response}")
            # LangChain clients typically return a BaseMessage object (like AIMessage)
            return {"messages": [response]} 
        except Exception as e:
            logger.error(f"Error during LLM invocation in ChatAgentWithTools: {str(e)}", exc_info=True)
            error_message = BaseMessage(role="assistant", content="I encountered an error processing your request. Please try again.")
            return {"messages": [error_message]}
