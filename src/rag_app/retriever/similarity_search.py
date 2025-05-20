
def init_similarity_search(state,vector_store):
    """
    Retrieves relevant documents from the vector store based on the input state.

    Args:
        state: The current state of the application.
        vector_store: The vector store to retrieve documents from.

    Returns:
        A list of retrieved documents.
    """
    # Extract the query from the state
    query = state['user_question']
    results = ["NO CONTEXT FOUND FOR THIS QUERY"]
    # Perform similarity search in the vector store
    results = vector_store.similarity_search(query)

    return {"context": results}