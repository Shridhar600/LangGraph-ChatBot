from typing import Optional

def isValidLLMConfig(provider: Optional[str], 
                           llm_api_key: Optional[str], 
                           llm_model: Optional[str]) -> bool:
    """ Validate the LLM configuration."""
    if provider == '' or llm_api_key == '' or llm_model == '': # Check if any of the values are empty strings.
        return False
    if provider not in ['gemini', 'openai']:
        return False
    return True