from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.documents import Document


class RagAgentState(TypedDict):
    """
    Represents the state of the graph, containing the history of messages.
    """
    user_question: str
    messages: Annotated[list, add_messages]
    context: List[Document]
