from settings.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import BaseLLMClient, BaseChatModel 
from utils.logger import logger

class GeminiClient(BaseLLMClient):
    """
    Concrete implementation of BaseLLMClient for Google Gemini models 
    using LangChain's ChatGoogleGenerativeAI.
    """
    def __init__(self):
        """
        Initializes the ChatGoogleGenerativeAI client using settings from Config.
        Handles potential errors during client instantiation.
        """
        try:
            self._client: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
                model=Config.LLM_MODEL,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=Config.LLM_KEY,
                # verbose=Config.DEBUG
            )
            logger.info(f"GeminiClient initialized successfully for model: {Config.LLM_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize GeminiClient: {e}", exc_info=True)
            raise  # Re-raise the exception to signal failure

    def get_client(self) -> BaseChatModel:
        """
        Returns the initialized ChatGoogleGenerativeAI instance.

        Returns:
            An instance of ChatGoogleGenerativeAI which conforms to BaseChatModel.
        """
        if not hasattr(self, '_client') or self._client is None:
             logger.error("GeminiClient's internal client is not initialized.")
             raise RuntimeError("GeminiClient was not initialized successfully.")
        return self._client
