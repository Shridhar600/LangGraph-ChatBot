from settings.config import Config
from llm_clients.gemini import GeminiClient

def getLLMClient() -> object:
    """ Returns a client for the LLM API."""
    if Config.LLM_PROVIDER.lower() == 'gemini':
        return GeminiClient()
    elif Config.LLM_PROVIDER.lower() == 'openai':
        pass