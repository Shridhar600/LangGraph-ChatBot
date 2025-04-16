from .baseLlmModel import BaseLlmModel
from src.chatBot_app.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

class ChatGemini(BaseLlmModel):
    def __init__(self, model_name: str, temperature: float = 0.7):
        """
        Initializes the ChatGemini client with the specified model name,
        temperature, and maximum tokens.

        Args:
            model_name (str): The name of the model to use.
            temperature (float): The sampling temperature.
            max_tokens (int): The maximum number of tokens to generate.
        """
        self.model_name = model_name if model_name else Config.GEMINI_MODEL
        self.temperature = temperature
        # self.max_tokens = max_tokens
        self.client = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            # max_tokens=self.max_tokens,
            api_key=Config.GEMINI_API_KEY,
        )


    def get_llm_client(self) -> BaseChatModel:
        """
        Returns the initialized ChatGoogleGenerativeAI instance.
        """
        if not hasattr(self, 'client') or self.client is None:
            raise RuntimeError("ChatGemini client is not initialized.")
        return self.client