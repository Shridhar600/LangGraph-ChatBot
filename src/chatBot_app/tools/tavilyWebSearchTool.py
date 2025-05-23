from typing import Optional # Optional will be removed as we raise error now
from langchain_community.tools.tavily_search import TavilySearchResults
from .. import Config
from ..utils import setup_logger
from ..utils.exceptions import ToolInitializationError

log = setup_logger(__name__)


def getTavilyWebSearchTool(maxResults: int = 2) -> TavilySearchResults: # Return type changed
    """
    Initialize the Tavily search tool with the API key from the configuration.
    Returns:
        TavilySearchResults: An instance of the Tavily search tool.
    """
    try:
        # You can customize max_results if needed
        tavily_tool = TavilySearchResults(
            max_results=maxResults, tavily_api_key=Config.TAVILY_API_KEY
        )
        log.info("Tavily search tool initialized successfully.")
        return tavily_tool
    except Exception as e:
        log.error(f"Failed to initialize Tavily search tool: {e}", exc_info=True)
        raise ToolInitializationError(f"Failed to initialize Tavily search tool: {e}") from e
