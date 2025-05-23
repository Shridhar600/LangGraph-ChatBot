from ..document_loaders import get_docs_from_url
from ..splitters import split_text_recursively
from ..embedding_models import create_embedding_model
from ..vector_store import get_vector_storage
from ..retriever import init_similarity_search
from ..vector_store.vector_store import VectorStore

from src.chatBot_app import setup_logger
from src.chatBot_app.utils.exceptions import DocumentLoadingError, EmbeddingError, VectorStoreError

log = setup_logger(__name__)

def rag_setup() -> VectorStore:
    """
    This function sets up the RAG (Retrieval-Augmented Generation) system.
    It initializes the necessary components and configurations.
    """
    log.info("Setting up RAG system...")
    url = "https://lilianweng.github.io/posts/2023-06-23-agent/"

    try:
        docs = get_docs_from_url(url)
    except Exception as e:
        log.error(f"Failed to load documents from URL '{url}': {e}", exc_info=True)
        raise DocumentLoadingError(f"Failed to load documents from URL '{url}': {e}") from e
    
    split_docs = split_text_recursively(docs)

    log.info(f"Number of documents: {len(docs)}")
    log.info(f"Number of split documents: {len(split_docs)}")
    
    #indexing the split documents
    try:
        embedding_model = create_embedding_model(None)
    except Exception as e:
        log.error(f"Failed to create embedding model: {e}", exc_info=True)
        raise EmbeddingError(f"Failed to create embedding model: {e}") from e

    try:
        vector_store = get_vector_storage(embedding_model)
    except Exception as e:
        log.error(f"Failed to get vector storage: {e}", exc_info=True)
        raise VectorStoreError(f"Failed to get vector storage: {e}") from e

    try:
        vector_store.add_documents(split_docs)
        log.info("Documents added to vector store successfully.")
    except Exception as e:
        log.error(f"Failed to add documents to vector store: {e}", exc_info=True)
        raise VectorStoreError(f"Failed to add documents to vector store: {e}") from e
        
    #This is a test to check if the documents are indexed correctly
    # docs2 = vector_store.similarity_search("What is Task Decomposition?", k=2)
    # log.info(f"Retrieved documents: {docs2[:3]}")
    
    log.info("RAG system setup complete.")
    return vector_store
