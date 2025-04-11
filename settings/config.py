import os
from dotenv import load_dotenv
from validation.validation import isValidLLMConfig

load_dotenv()

ENV = os.environ.get("ENV", "dev")  # Default to 'dev' if not set

if ENV == "prod":
    from dotenv import find_dotenv
    load_dotenv(dotenv_path=".env.production", override= True)  # Load the .env file in production mode and override the earlier values. 

class BaseConfig:
    LLM_KEY = os.environ.get("LLM_KEY")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"  # Default to False, the == compares the string to "true" making the DEBUG variable a boolean.
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER")
    LLM_MODEL = os.environ.get("LLM_MODEL")

    if not isValidLLMConfig(LLM_PROVIDER, LLM_KEY, LLM_MODEL):  # Validate the LLM configuration
        raise ValueError("Invalid LLM configuration. Please check your .env variables.")
    elif DEBUG:  # If DEBUG is True, print a validation message.
        print("LLM configuration is valid.")

class DevConfig(BaseConfig):  
    env:str = "dev"

class ProdConfig(BaseConfig): 
    env:str = "prod"

Config = ProdConfig if ENV == "prod" else DevConfig # here we not using an instance of the class but rather the class itself.

# Example usage:
# from config import Config
# print(Config.LLM_KEY)  # Access the LLM_KEY from the loaded config
# print(Config.DEBUG)  # Access the DEBUG flag from the loaded config
# print(Config.env)  # Access the environment (dev or prod)