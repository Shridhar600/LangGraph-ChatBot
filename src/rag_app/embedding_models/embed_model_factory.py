from src.rag_app.embedding_models.ollama_embed import OllamaEmbeddingModel
from src.chatBot_app import setup_logger
from typing import Optional

log = setup_logger(__name__)

def create_embedding_model(model_name: Optional[str] ):

    if True:
        embed_model = OllamaEmbeddingModel(model_name=model_name).get_embedding_model()
        log.info(f"Using embedding model: {embed_model.model}")
    return embed_model
