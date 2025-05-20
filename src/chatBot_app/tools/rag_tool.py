from langchain_core.tools import tool
from ..utils import setup_logger
from src.rag_app.core import rag_setup

log = setup_logger(__name__)

@tool(response_format="content_and_artifact")
def retrieve_user_corpous(query: str):
    """
    Retrieves relevant documents from the vector store based on the input query.
    Args:
        query: The query to search for in the vector store. 
    """
    log.info(f"Retrieving documents for query: {query}")
    retrieved_docs = rag_setup().similarity_search(query, k=2)
    log.info(f"LLM retrieved {len(retrieved_docs)} documents with the query: {query}")
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs # here serialized is the content and retrieved_docs is the artifact.


# response_format – The tool response format. If “content” then the output of the tool is interpreted as the contents of a ToolMessage. 
#If “content_and_artifact” then the output is expected to be a two-tuple corresponding to the (content, artifact) of a ToolMessage.
# Defaults to “content”.