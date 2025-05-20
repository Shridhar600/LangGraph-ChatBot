from langchain_core.vectorstores import VectorStore as LangchainVectorStore
from src.chatBot_app import setup_logger

log = setup_logger(__name__)

class VectorStore:
    def __init__(self,vector_store: LangchainVectorStore):
        # self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.is_indexed = False

    def add_documents(self, langchain_docs):
        """ Adds documents to the vector store. """
        ids = self.vector_store.add_documents(langchain_docs)
        self.is_indexed = True
        log.info(f"Number of documents in vector store: {len(ids)}")
        return ids

    def similarity_search(self, query, k=2):
        if not self.is_indexed:
            raise RuntimeError("Vector store is not indexed. Add documents first.")
        return self.vector_store.similarity_search(query, k=k)

    def get_underlying(self):
        return self.vector_store
