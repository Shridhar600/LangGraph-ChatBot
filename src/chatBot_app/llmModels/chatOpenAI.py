from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI as LangchainChatOpenAI # Alias to avoid naming conflict
from .baseLlmModel import BaseLlmModel
from src.chatBot_app.config import Config
from ..utils import setup_logger
from ..utils.exceptions import LLMInitializationError, InvalidStateError

log = setup_logger(__name__)

class ChatOpenAI(BaseLlmModel):
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """
        Initializes the ChatOpenAI client.

        Args:
            model_name (str, optional): The name of the model to use. 
                                        Defaults to Config.OPENAI_MODEL.
            temperature (float, optional): The sampling temperature. Defaults to 0.7.
        """
        self.model_name = model_name if model_name else Config.OPENAI_MODEL
        self.temperature = temperature
        
        if not Config.OPENAI_API_KEY:
            log.error("OPENAI_API_KEY is not configured.")
            raise LLMInitializationError("OPENAI_API_KEY is not configured.")

        try:
            self.client = LangchainChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=Config.OPENAI_API_KEY
                # Other parameters like max_tokens can be added if needed
            )
            log.info(f"ChatOpenAI client initialized successfully with model: {self.model_name}")
        except Exception as e:
            log.error(f"Failed to initialize LangchainChatOpenAI: {e}", exc_info=True)
            raise LLMInitializationError(f"Failed to initialize LangchainChatOpenAI: {e}") from e

    def get_llm_client(self) -> BaseChatModel:
        """
        Returns the initialized LangchainChatOpenAI instance.

        Raises:
            InvalidStateError: If the client is not initialized.
        """
        if not hasattr(self, "client") or self.client is None:
            log.error("ChatOpenAI client is not initialized or 'client' attribute is missing.")
            raise InvalidStateError("ChatOpenAI client is not initialized.")
        # The log message from __init__ already confirms successful initialization and model.
        # If we want to log every time get_llm_client is called, we can add:
        # log.info(f"Returning ChatOpenAI client for model: {self.model_name}")
        return self.client

    # Placeholder for other methods like invoke, stream if they were part of BaseLlmModel
    # def invoke(self, messages):
    #     if not self.client:
    #         raise InvalidStateError("Client not initialized")
    #     try:
    #         # ... logic ...
    #     except Exception as e:
    #         raise LLMAPIError("Failed during OpenAI invoke") from e

    # def stream(self, messages):
    #     if not self.client:
    #         raise InvalidStateError("Client not initialized")
    #     try:
    #         # ... logic ...
    #     except Exception as e:
    #         raise LLMAPIError("Failed during OpenAI stream") from e
