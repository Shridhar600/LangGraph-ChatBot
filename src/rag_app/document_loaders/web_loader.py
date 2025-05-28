import bs4
from langchain_community.document_loaders import WebBaseLoader

def web_loader(url: str) -> WebBaseLoader:
    """
    Loads a web page from the specified URL.

    Args:
        url (str): The URL of the web page to load.

    Returns:
        WebBaseLoader: An instance of WebBaseLoader for the specified URL.
    """
    bs4_strainer = get_bs4_strainer()
    web_loader = WebBaseLoader(web_path=url,  bs_kwargs={"parse_only": bs4_strainer})
    return web_loader


def get_bs4_strainer():
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    return bs4_strainer

def get_docs_from_url(url: str) -> list:
    """
    Fetches documents from the specified URL.

    Args:
        url (str): The URL of the web page to fetch documents from.

    Returns:
        list: A list of documents fetched from the web page.
    """
    web_loader_instance = web_loader(url)
    docs = web_loader_instance.load()
    return docs