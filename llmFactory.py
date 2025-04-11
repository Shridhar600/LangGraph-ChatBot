from typing import Optional, Type 
from settings.config import Config
from llm_clients.base import BaseLLMClient 
from llm_clients.gemini import GeminiClient
from utils.logger import logger

# --- LLM Client Registry ---
# Dictionary mapping provider names (lowercase) to their client classes.
# Add new providers here.
LLM_CLIENT_REGISTRY: dict[str, Type[BaseLLMClient]] = {
    "gemini": GeminiClient,
    # "openai": OpenAIClient,
}

# --- Factory Function ---
def getLLMClient() -> Optional[BaseLLMClient]:
    """ 
    Factory function to get an instance of the appropriate LLM client wrapper 
    based on the configuration.

    Returns:
        An instance of a BaseLLMClient subclass (e.g., GeminiClient), 
        or None if the provider is not configured, not supported, or 
        if initialization fails within the client's __init__.
    """
    provider = Config.LLM_PROVIDER
    if not provider:
        logger.error("LLM_PROVIDER is not set in the configuration.")
        return None

    provider_lower = provider.lower()
    # logger.info(f"Attempting to get LLM client for provider: {provider_lower}")

    # Look up the client class in the registry
    client_class = LLM_CLIENT_REGISTRY.get(provider_lower)

    if client_class:
        try:
            # Instantiate the client class
            client_instance = client_class() 
            logger.info(f"Successfully created LLM client instance for provider: {provider_lower}")
            return client_instance
        except Exception as e:
            # Catch potential errors during client instantiation (e.g., invalid API key)
            # The client's __init__ should ideally log specific errors.
            logger.error(f"Failed to instantiate LLM client for provider '{provider_lower}': {e}", exc_info=True)
            return None # Return None if instantiation fails
    else:
        # Provider not found in the registry
        logger.error(f"Unsupported LLM_PROVIDER configured: '{provider}'. Supported providers are: {list(LLM_CLIENT_REGISTRY.keys())}")
        return None
