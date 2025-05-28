from src.rag_app.vector_store.vector_store import VectorStore
from langchain_core.vectorstores import InMemoryVectorStore
from src.chatBot_app import setup_logger

log = setup_logger(__name__)


def get_vector_storage(embeddings, **kwargs):
    # will implement a factory method to create the vector store based on environmental Configurations.
    if True:
       vector_store = VectorStore(InMemoryVectorStore(embeddings))
       log.info(f"Using InMemory Vector Store")
       return vector_store
