from typing import Type
from langchain_core.language_models.chat_models import BaseChatModel
from .chatGemini import ChatGemini
from .chatOpenAI import ChatOpenAI
from src.chatBot_app.config import Config

def create_llm_client() -> BaseChatModel:
    """ Returns an instance of a language model client based on the specified type. """
    provider = (Config.LLM_PROVIDER).lower() # Validation handled in config.py

    if provider == "gemini":
        client = ChatGemini().get_llm_client() 
        return client
    elif provider == "openai":
        client = ChatOpenAI().get_llm_client() 
        return client
        
    raise ValueError(f"Unsupported LLM provider: {provider}")
