from typing import Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from .. import Config
from ..utils import setup_logger

log = setup_logger(__name__)


def getTavilyWebSearchTool(maxResults: int = 3) -> Optional[TavilySearchResults]:
    """
    Initialize the Tavily search tool with the API key from the configuration.
    Returns:
        TavilySearchResults: An instance of the Tavily search tool.
    """
    try:
        # You can customize max_results if needed
        tavily_tool = TavilySearchResults(
            max_results=2, tavily_api_key=Config.TAVILY_API_KEY
        )
        log.info("Tavily search tool initialized successfully.")
        return tavily_tool
    except Exception as e:
        log.error(f"Failed to initialize Tavily search tool: {e}", exc_info=True)
        # Set tool to None if initialization fails, so downstream code can check
        return None
