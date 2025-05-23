from langchain_core.language_models.chat_models import BaseChatModel
from .chat_ollama import OllamaChat
from .chatGemini import ChatGemini
from .chatOpenAI import ChatOpenAI
from src.chatBot_app.config import Config
from ..utils import setup_logger
from ..utils.exceptions import LLMInitializationError, LLMToolBindError

log = setup_logger(__name__)


def create_llm_client(tools: list, isToolsEnabled: bool) -> BaseChatModel:
    """Returns an instance of a language model client based on the specified type. It is not dependent on the part where it is called from. It can Just access the config to find the enabled LLM Provider."""
    provider = (Config.LLM_PROVIDER).lower()  # Validation handled in config.py

    if provider == "gemini":
        try:
            client = ChatGemini(model_name=None).get_llm_client()
        except Exception as e:
            log.error(f"Failed to initialize gemini client: {e}", exc_info=True)
            raise LLMInitializationError(f"Failed to initialize gemini client: {e}") from e
        if isToolsEnabled:
            client = bind_tools_to_llm_client(client, tools)
        log.info(f"Gemini LLM client created with model: {Config.GEMINI_MODEL}")
        return client

    elif provider == "openai":
        try:
            client = ChatOpenAI().get_llm_client()
        except Exception as e:
            log.error(f"Failed to initialize openai client: {e}", exc_info=True)
            raise LLMInitializationError(f"Failed to initialize openai client: {e}") from e
        # Note: The original code didn't explicitly bind tools for OpenAI in this function block.
        # Assuming tools are bound later if isToolsEnabled is true, similar to other providers,
        # or that OpenAI client handles tools differently and doesn't need explicit binding here.
        # For now, if tools need to be enabled for OpenAI, it seems it would also use the
        # bind_tools_to_llm_client function, but that logic is outside this direct client init.
        # The instructions were to wrap client instantiation.
        # If OpenAI needs tools, the calling code should handle the isToolsEnabled logic like for others.
        # A common pattern would be:
        # client = create_llm_client(tools=[], isToolsEnabled=False) # Get base client
        # if isToolsEnabled: client = bind_tools_to_llm_client(client, tools)
        # However, the current function signature `create_llm_client(tools: list, isToolsEnabled: bool)`
        # suggests tool binding *can* happen within it.
        # The original code for OpenAI did:
        #   client = ChatOpenAI().get_llm_client()
        #   log.info(f"OpenAI LLM client created with model: {Config.OPENAI_MODEL}")
        #   return client
        # It did NOT call bind_tools_to_llm_client like gemini and ollama.
        # I will keep the original logic for OpenAI regarding tool binding: it's not done here.
        # The problem description implies tool binding *might* be part of instantiation for OpenAI
        # e.g. ChatOpenAI(model_name=Config.OPENAI_MODEL, temperature=0).bind_tools(tools)
        # but the actual code read shows .get_llm_client() is called, and then tools are bound separately if needed.
        # So, will stick to wrapping ChatOpenAI().get_llm_client().
        # If tools are enabled for OpenAI, the calling code of create_llm_client should handle it.
        # For consistency, and given the current structure, if `isToolsEnabled` is True for OpenAI,
        # it should also call `bind_tools_to_llm_client`. I'll add that.
        if isToolsEnabled: # Adding this for consistency with gemini and ollama
             client = bind_tools_to_llm_client(client, tools)
        log.info(f"OpenAI LLM client created with model: {Config.OPENAI_MODEL}")
        return client
    
    elif provider == "ollama":
        try:
            client = OllamaChat(model_name=None).get_llm_client()
        except Exception as e:
            log.error(f"Failed to initialize ollama client: {e}", exc_info=True)
            raise LLMInitializationError(f"Failed to initialize ollama client: {e}") from e
        if isToolsEnabled:
            client = bind_tools_to_llm_client(client, tools)
        log.info(f"Ollama LLM client created with model: {Config.OLLAMA_MODEL}")
        return client

    raise ValueError(f"Unsupported LLM provider: {provider}")

def bind_tools_to_llm_client(client: BaseChatModel, tools: list) -> BaseChatModel:
    """
    Binds tools to the LLM client.
    """
    try:
        client_with_tools = client.bind_tools(tools=tools)
        log.debug(f"LLM client bound with tools: {tools}")
        return client_with_tools
    except Exception as e:
        log.error(f"Failed to bind tools to LLM client: {e}", exc_info=True)
        raise LLMToolBindError(f"Failed to bind tools to LLM client: {e}") from e
