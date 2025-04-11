from abc import ABC, abstractmethod
# Import the base class for LangChain chat models
from langchain_core.language_models.chat_models import BaseChatModel 

class BaseLLMClient(ABC):
    """
    Abstract Base Class for LLM client wrappers.
    Ensures concrete implementations provide a way to get a LangChain chat model instance.
    """
    @abstractmethod
    def __init__(self) -> None:
        """Initializes the LLM client wrapper."""
        pass

    @abstractmethod
    def get_client(self) -> BaseChatModel:
        """
        Returns the underlying LangChain LLM client instance (e.g., ChatGoogleGenerativeAI).
        """
        pass
