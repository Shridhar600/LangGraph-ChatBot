from abc import ABC, abstractmethod
from typing import Any

class BaseLLMClient(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_client(self) -> Any:
        """Returns the LLM client instance"""
        pass
