from langchain_ollama import ChatOllama
from .baseLlmModel import BaseLlmModel
from src.chatBot_app.config import Config
from langchain_core.language_models.chat_models import BaseChatModel
from ..utils import setup_logger
from ..utils.exceptions import LLMInitializationError, InvalidStateError

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
        try:
            self.client = ChatOllama(
                    model=self.model_name,
                    temperature=self.temperature,
                )
            log.info(f"ChatOllama client initialized successfully with model: {self.model_name}")
        except Exception as e:
            log.error(f"Failed to initialize ChatOllama: {e}", exc_info=True)
            raise LLMInitializationError(f"Failed to initialize ChatOllama: {e}") from e

    def get_llm_client(self) -> BaseChatModel:
        """
        Returns the initialized ChatOllama instance.
        """
        if not hasattr(self, "client") or self.client is None:
            log.error("ChatOllama client is not initialized or 'client' attribute is missing.")
            raise InvalidStateError("ChatOllama client is not initialized.")
        log.info(f"Returning ChatOllama client for model: {self.model_name}")
        return self.client
