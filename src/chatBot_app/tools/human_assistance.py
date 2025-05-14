from langgraph.types import interrupt
from langchain_core.tools import tool
from ..utils import setup_logger

log = setup_logger(__name__)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human. If you are unsure, or the query requires subjective judgment, you can ask for human assistance."""
    log.debug(f"Requesting human assistance for query: {query}")
    human_response = interrupt({"The LLM has asked the user: ": query}) # ye ek input() ki trh and iska response we will pass through Command.  
    return human_response["data"]