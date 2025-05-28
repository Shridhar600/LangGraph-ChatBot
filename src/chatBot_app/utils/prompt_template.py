from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .prompts import CHATBOT_SYSTEM_PROMPT


def create_prompt_template(system_prompt: str = CHATBOT_SYSTEM_PROMPT) -> ChatPromptTemplate:
    """
    Creates a chat prompt template with a configurable system prompt.

    Args:
        system_prompt: The system prompt to use in the template.  Defaults to CHATBOT_SYSTEM_PROMPT

    Returns:
        A ChatPromptTemplate instance.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            # SystemMessage(content=system_prompt),
            ("system",system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt_template