from langchain_core.vectorstores import VectorStore as LangchainVectorStore
from src.chatBot_app import setup_logger
from src.chatBot_app.utils.exceptions import VectorStoreError, InvalidStateError

log = setup_logger(__name__)

class VectorStore:
    def __init__(self,vector_store: LangchainVectorStore):
        # self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.is_indexed = False

    def add_documents(self, langchain_docs):
        """ Adds documents to the vector store. """
        try:
            ids = self.vector_store.add_documents(langchain_docs)
            self.is_indexed = True
            log.info(f"Successfully added {len(ids)} documents to vector store.")
            return ids
        except Exception as e:
            log.error(f"Failed to add documents to underlying vector store: {e}", exc_info=True)
            raise VectorStoreError(f"Failed to add documents to underlying vector store: {e}") from e

    def similarity_search(self, query, k=2):
        if not self.is_indexed:
            log.warning("Similarity search called on a non-indexed vector store.")
            raise InvalidStateError("Vector store is not indexed. Add documents first.")
        try:
            results = self.vector_store.similarity_search(query, k=k)
            log.info(f"Similarity search for query '{query}' (k={k}) returned {len(results)} results.")
            return results
        except Exception as e:
            log.error(f"Failed during similarity search in underlying vector store for query '{query}': {e}", exc_info=True)
            raise VectorStoreError(f"Failed during similarity search in underlying vector store for query '{query}': {e}") from e

    def get_underlying(self):
        return self.vector_store
