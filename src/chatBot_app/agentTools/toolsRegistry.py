from .tavilyWebSearchTool import getTavilyWebSearchTool


def get_tools() -> list:
    """
    Get a list of tools for the chatbot.
    
    Returns:
        list: A list of tool instances.
    """
    # Initialize the tools
    tavily_tool = getTavilyWebSearchTool()
    # wikipedia_tool = getWikipediaSearchTool()

    # Return the tools as a list
    return [tavily_tool] 