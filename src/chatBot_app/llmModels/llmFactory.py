from typing import Type
from langchain_core.language_models.chat_models import BaseChatModel
from .chatGemini import ChatGemini
from .chatOpenAI import ChatOpenAI
from src.chatBot_app.config import Config
from ..utils import setup_logger

log = setup_logger(__name__)

def create_llm_client(tools: list, isToolsEnabled: bool) -> BaseChatModel:
    """ Returns an instance of a language model client based on the specified type. It is not dependent on the part where it is called from. It can Just access the config to find the enabled LLM Provider. """
    provider = (Config.LLM_PROVIDER).lower() # Validation handled in config.py

    if provider == "gemini":
        client = ChatGemini(model_name=None).get_llm_client() 
        if isToolsEnabled:
            client = client.bind_tools(tools=tools)
            return client
        log.info(f"Gemini LLM client created with model: {Config.GEMINI_MODEL}")
        return client
    
    elif provider == "openai":
        client = ChatOpenAI().get_llm_client() 
        log.info("OpenAI LLM client created with model: {Config.OPENAI_MODEL}")
        return client
        
    raise ValueError(f"Unsupported LLM provider: {provider}")