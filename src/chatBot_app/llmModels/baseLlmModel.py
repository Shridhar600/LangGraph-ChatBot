from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel


class BaseLlmModel(ABC):
    """will probably destroy this class and use the langchain base class directly"""
    @abstractmethod
    def get_llm_client(self) -> BaseChatModel:
        """
        Returns the LLM client instance.
        """
        pass