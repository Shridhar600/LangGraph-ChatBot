from settings.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import BaseLLMClient

class GeminiClient(BaseLLMClient):
    def __init__(self):
        self._client = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=Config.LLM_KEY,
            verbose=Config.DEBUG
        )
    
    def get_client(self) -> ChatGoogleGenerativeAI:
        """Returns the LLM client instance"""
        return self._client

