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
    tavily_tool = getTavilyWebSearchTool()
    
    tools = {
        "tavilyWebSearchTool": tavily_tool
    }
    
    valid_tools = []
    for name, tool in tools.items():
        if CommonUtils.isValidTool(tool):
            valid_tools.append(tool)
             
    log.info("List of Active Tools: %s", [tool.__class__.__name__ for tool in valid_tools])
    return valid_tools
