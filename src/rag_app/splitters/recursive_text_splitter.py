from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_recursively(docs: list, chunk_size: int = 1000, chunk_overlap: int = 200, add_start_index=True) -> list:
    """
    Splits the input documents into smaller chunks using a recursive character text splitter.

    Args:
        docs (list): The input documents to be split.
        chunk_size (int): The maximum size of each chunk. Default is 1000.
        chunk_overlap (int): The number of overlapping characters between chunks. Default is 200.

    Returns:
        list: A list of Langchain Document objects, each representing a chunk of the original documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=add_start_index
    )
    return text_splitter.split_documents(docs)

