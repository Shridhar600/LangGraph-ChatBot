from langchain_core.vectorstores import InMemoryVectorStore


class InMemoryVectorStorage:
    def __init__(self, embeddings):
        """
        Initializes the InMemoryVectorStorage with the specified embeddings.
        """
        self.vector_store = InMemoryVectorStore(embeddings)

