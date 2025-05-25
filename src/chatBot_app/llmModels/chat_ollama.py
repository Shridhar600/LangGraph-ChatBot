from langchain_ollama import ChatOllama
from .baseLlmModel import BaseLlmModel
from src.config import Config
from langchain_core.language_models.chat_models import BaseChatModel
from ..utils import setup_logger

log = setup_logger(__name__)

class OllamaChat(BaseLlmModel):
    def __init__(self, model_name: str, temperature: float = 0.7):
        """
        Initializes the ChatOllama client with the specified model name and temperature.

        Args:
            model_name (str): The name of the model to use.
            temperature (float): The sampling temperature.
        """
        self.model_name = model_name if model_name else Config.OLLAMA_MODEL
        self.temperature = temperature
        self.client = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
            )

    def get_llm_client(self) -> BaseChatModel:
        """
        Returns the initialized ChatOllama instance.
        """  
        log.debug(f"ChatOllama client initialized with model: {self.model_name}")
        return self.client
