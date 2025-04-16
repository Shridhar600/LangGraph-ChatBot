from utils.logger import logger

def getToolsForLLM() -> list:
    """ 
    Factory function to get a list of tools for the LLM client.
    
    Returns:
        A list of tool instances that can be bound to the LLM client.
    """
    tools = []

    try:
        from tools.tavily import getTavilyWebSearchTool 
        tavily_tool = getTavilyWebSearchTool() # Initialize the Tavily search tool
        if tavily_tool:
            tools.append(tavily_tool) # Add the tool to the list
            logger.info("Tavily web search tool added successfully.")
        else:
            logger.warning("Failed to initialize Tavily web search tool.")
    except ImportError as e:
        logger.error(f"Tavily web search tool import failed: {e}", exc_info=True)
    
    return tools

