from langgraph.types import interrupt
from langchain_core.tools import tool
from ..utils import setup_logger

log = setup_logger(__name__)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    log.debug(f"Requesting human assistance for query: {query}")
    human_response = interrupt({"query": query})
    return human_response["data"]