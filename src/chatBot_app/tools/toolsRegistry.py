from .tavilyWebSearchTool import getTavilyWebSearchTool
from ..utils import CommonUtils
from ..utils import setup_logger

log = setup_logger(__name__)

def get_tools() -> list:
    """
    Get a list of tools for the chatbot.
    Returns:
        list: A list of tool instances.
    """
    tools = []
    
    tavily_tool = getTavilyWebSearchTool()
    CommonUtils.isValidTool(tools, tavily_tool)

    # wikipedia_tool = getWikipediaSearchTool()

    log.info("Active list of tools: %s", tools)
    return tools

