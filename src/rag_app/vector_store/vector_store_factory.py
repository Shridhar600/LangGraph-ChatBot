from .in_memory_vector_store import InMemoryVectorStorage

def get_vector_storage(embeddings, **kwargs):
    """
    Factory function to create a vector store based on the specified type.

    Args:
        vector_store_type (str): The type of vector store to create.
        embeddings: The embedding model to use.
        **kwargs: Additional arguments for the vector store.

    Returns:
        An instance of the specified vector store.
    """
        # For now, we only support InMemoryVectorStorage
    if True:
        vector_store = InMemoryVectorStorage(embeddings=embeddings).vector_store
        return vector_store
    
    # Add other vector store types as needed
    raise ValueError(f"Unsupported vector store type: {vector_store_type}")