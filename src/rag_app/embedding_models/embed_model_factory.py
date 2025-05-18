from .ollama_embed import OllamaEmbeddingModel

def create_embedding_model(model_name: str):

    if True:
        embed_model = OllamaEmbeddingModel(model_name=model_name).get_embedding_model()
    return embed_model
