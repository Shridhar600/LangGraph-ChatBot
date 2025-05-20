from ..document_loaders import get_docs_from_url
from ..splitters import split_text_recursively
from ..embedding_models import create_embedding_model
from ..vector_store import get_vector_storage
from ..retriever import init_similarity_search
from langchain_core.vectorstores import InMemoryVectorStore

from src.chatBot_app import setup_logger

log = setup_logger(__name__)

def rag_setup() ->InMemoryVectorStore:
    """
    This function sets up the RAG (Retrieval-Augmented Generation) system.
    It initializes the necessary components and configurations.
    """
    log.info("Setting up RAG system...")

    docs = get_docs_from_url("https://lilianweng.github.io/posts/2023-06-23-agent/")
    split_docs = split_text_recursively(docs)

    log.info(f"Number of documents: {len(docs)}")
    log.info(f"Number of split documents: {len(split_docs)}")
    log.info("RAG system setup complete.")
    
    #indexing the split documents

    embedding_model = create_embedding_model(None)
    log.info(f"Using embedding model: {embedding_model.model}")

    vector_store = get_vector_storage(embedding_model)
    log.info(f"Using vector store: {vector_store.__class__.__name__}")

    document_ids = vector_store.add_documents(documents=split_docs)
    log.info(f"Number of documents in vector store: {document_ids[:3]}")

    docs2 = init_similarity_search({"user_question":"What is Task Decomposition?"}, vector_store)
    log.info(f"Retrieved documents: {docs2['context'][:3]}")
    
    return vector_store
