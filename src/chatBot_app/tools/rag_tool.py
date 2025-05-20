from langchain_core.tools import tool
from ..utils import setup_logger
from src.rag_app.core.vector_store_singleton import VECTOR_STORE

log = setup_logger(__name__)

@tool(response_format="content_and_artifact")
def retrieve_user_corpous(query: str):
    """
    Retrieves semantically relevant documents from the user-specific vector store based on the input query. Use this tool to access user-uploaded documents or internal knowledge bases.

    This tool performs a similarity search against an internal vector store containing private or organization-specific documents.
    It is useful for answering questions related to proprietary content, internal knowledge, or user-uploaded data.

    Args:
        query (str): A natural language question or keyword phrase representing the user's intent. 
                     This query will be used to perform a vector similarity search to find relevant documents.

    Returns:
        Tuple[str, List[Document]]: 
            - A serialized string containing the metadata and content of the top-matching documents, formatted for LLM consumption.
            - A list of raw `Document` objects for downstream use, including metadata and page content.

    Example:
        User Query: "What are the internal guidelines for submitting quarterly reports?"
        Returned: Top 2 documents containing relevant content and metadata.

    Notes:
        - The search is limited to the top 2 results (`k=2`) for concise context retrieval.
        - This tool is best suited for queries requiring access to user-uploaded corpora or internal knowledge bases.
    """
    
    log.info(f"Retrieving documents for query: {query}")
    retrieved_docs = VECTOR_STORE.similarity_search(query, k=2)
    log.info(f"LLM retrieved {len(retrieved_docs)} documents with the query: {query}")
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs # here serialized is the content and retrieved_docs is the artifact.


# response_format – The tool response format. If “content” then the output of the tool is interpreted as the contents of a ToolMessage. 
#If “content_and_artifact” then the output is expected to be a two-tuple corresponding to the (content, artifact) of a ToolMessage.
# Defaults to “content”.