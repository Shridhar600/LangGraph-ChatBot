from .tavilyWebSearchTool import getTavilyWebSearchTool
from utils import CommonUtils

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

    return tools

