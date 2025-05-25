from src.rag_app.document_loaders import get_docs_from_url
from src.rag_app.splitters import split_text_recursively
from src.rag_app.embedding_models import create_embedding_model
from src.rag_app.vector_store import get_vector_storage
from src.rag_app.retriever import init_similarity_search
from src.rag_app.vector_store.vector_store import VectorStore

from src.chatBot_app import setup_logger

log = setup_logger(__name__)

def rag_setup() -> VectorStore:
    """
    This function sets up the RAG (Retrieval-Augmented Generation) system.
    It initializes the necessary components and configurations.
    """
    log.info("Setting up RAG system...")

    docs = get_docs_from_url("https://lilianweng.github.io/posts/2023-06-23-agent/")
    split_docs = split_text_recursively(docs)

    log.info(f"Number of documents: {len(docs)}")
    log.info(f"Number of split documents: {len(split_docs)}")
    
    #indexing the split documents

    embedding_model = create_embedding_model(None)

    vector_store = get_vector_storage(embedding_model)

    vector_store.add_documents(split_docs)
    #This is a test to check if the documents are indexed correctly
    # docs2 = vector_store.similarity_search("What is Task Decomposition?", k=2)
    # log.info(f"Retrieved documents: {docs2[:3]}")
    
    log.info("RAG system setup complete.")
    return vector_store
