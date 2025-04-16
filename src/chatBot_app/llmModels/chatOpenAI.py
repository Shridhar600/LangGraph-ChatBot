from langchain_core.language_models.chat_models import BaseChatModel
from chatBot_app.llmModels.baseLlmModel import BaseLlmModel

class ChatOpenAI(BaseLlmModel):
    pass

    def getLLMClient(self) -> BaseChatModel:
        pass