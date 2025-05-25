from src import start_cli,test_connection

from src.rag_app.core.vector_store_singleton import VECTOR_STORE  # Ensure vector store is initialized at startup

if __name__ == "__main__":
    # start_cli()
    test_connection()
