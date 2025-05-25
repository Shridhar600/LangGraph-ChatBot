# Holds a singleton instance of the vector store for the RAG pipeline
from src.rag_app.core.rag_setup import rag_setup

# Build the vector store ONCE at startup
VECTOR_STORE = rag_setup()
