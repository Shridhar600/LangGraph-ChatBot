import os
import logging # Import standard logging
from typing import Literal, Tuple, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get a logger specific to this module
config_logger = logging.getLogger(__name__)

# --- Environment Detection ---
# Determine the environment ('dev' or 'prod')
# Default to 'dev' if ENV environment variable is not set.
ENV: str = os.environ.get("ENV", "dev").lower()

# Define the .env files to load based on the environment.
# Files listed later in the tuple override values from earlier files.
# Environment variables always take precedence over .env files.
env_files_to_load: Tuple[str, ...] = ('.env',) # Base .env file is always loaded

if ENV == "prod":
    env_files_to_load += ('.env.production',) # Load production overrides
    config_logger.info("Production environment detected (ENV=prod). Loading .env and .env.production")
elif ENV == "dev":
     config_logger.info("Development environment detected (ENV=dev). Loading .env")
else:
     config_logger.warning(f"Unknown environment detected (ENV={ENV}). Loading only .env")
     # Consider raising an error if only 'dev' or 'prod' are acceptable


# --- Pydantic Settings Model ---
class AppSettings(BaseSettings):
    """
    Defines application settings using Pydantic for validation and type safety.
    Loads settings from environment variables and specified .env files.
    """
    # --- Environment ---
    # Store the detected environment within the settings object itself
    ENV: str = ENV 

    # --- LLM Configuration ---
    # These fields are required. Pydantic will raise a validation error
    # if they are not found in environment variables or the loaded .env files.
    LLM_KEY: str 
    LLM_MODEL: str 
    # Use Literal to restrict the allowed values for the provider
    LLM_PROVIDER: Literal['gemini', 'openai'] 

    # --- Debugging ---
    # Optional setting with a default value.
    # Pydantic automatically converts "true"/"false", 1/0 to boolean.
    DEBUG: bool = False

    # --- Pydantic Model Configuration ---
    model_config = SettingsConfigDict(
        env_file=env_files_to_load,      # Tuple of .env files to load
        env_file_encoding='utf-8',     # Specify encoding for .env files
        case_sensitive=False,          # Match environment variables case-insensitively
        extra='ignore'                 # Ignore extra variables found in the environment or .env files
    )

# --- Instantiate and Validate Settings ---
# Create a single instance of the settings. This is where Pydantic performs
# the loading from .env/environment and validates the data against the model.
# This instance will be imported by other modules in the application.
try:
    Config = AppSettings()
    # Log successful loading, potentially masking sensitive keys if DEBUG is true
    if Config.DEBUG:
        # Create a dictionary representation, masking the API key
        debug_config_dict = Config.model_dump()
        debug_config_dict['LLM_KEY'] = '********' if debug_config_dict.get('LLM_KEY') else None
        config_logger.debug(f"Configuration loaded successfully: {debug_config_dict}")
    else:
        config_logger.info("Configuration loaded successfully.")

except Exception as validation_error:
    # Catch any validation errors from Pydantic during instantiation
    config_logger.error(f"CRITICAL: Failed to load or validate application configuration. Error: {validation_error}", exc_info=True)
    # Re-raise a more general error to halt execution if config is invalid
    raise ValueError(f"Configuration error - please check environment variables and .env files: {validation_error}") from validation_error

# The old BaseConfig, DevConfig, ProdConfig, and isValidLLMConfig are no longer needed.
# The `Config` object above is now the single source of truth for settings.
