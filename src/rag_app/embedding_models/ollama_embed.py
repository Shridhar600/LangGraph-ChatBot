from langchain_ollama import OllamaEmbeddings
from src.chatBot_app import Config, setup_logger
from typing import Optional

log = setup_logger(__name__)


class OllamaEmbeddingModel:
    """
    This class is a wrapper for the Ollama Embeddings model.
    It initializes the model with a specified model name.
    """

    def __init__(self, model_name: Optional[str]):
        """
        Initializes the OllamaEmbeddingModel with the specified model name.

        Args:
            model_name (str): The name of the model to use.
        """
        self.model_name = model_name if model_name else Config.OLLAMA_EMBEDDING_MODEL
        self.client = OllamaEmbeddings(model=self.model_name)

    def get_embedding_model(self):
        """
        Returns an instance of the OllamaEmbeddings model.
        """
        return self.client
