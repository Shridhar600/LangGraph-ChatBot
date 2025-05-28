import os
import logging
from typing import Tuple, Optional
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
env_files_to_load: Tuple[str, ...] = (".env",)  # Base .env file is always loaded

if ENV == "prod":
    env_files_to_load += (".env.production",)  # Load production overrides
    config_logger.info(
        "Production environment detected (ENV=prod). Loading .env and .env.production"
    )
elif ENV == "dev":
    config_logger.info("Development environment detected (ENV=dev). Loading .env")
else:
    config_logger.warning(
        f"Unknown environment detected (ENV={ENV}). Loading only .env"
    )
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
    GEMINI_API_KEY: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    OPENAI_API_KEY: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    GEMINI_MODEL: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    OPENAI_MODEL: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    OLLAMA_MODEL: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    OLLAMA_EMBEDDING_MODEL: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )

    POSTGRES_DB: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    POSTGRES_USER: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    POSTGRES_PASSWORD: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    POSTGRES_HOST: Optional[str] = (
        None  # Optional, can be set in .env or environment variables
    )
    POSTGRES_PORT: Optional[int] = (
        None  # Optional, can be set in .env or environment variables
    )
    LLM_PROVIDER: str  # Default LLM provider

    # --- LLM Configuration ---
    # These fields are required. Pydantic will raise a validation error
    # if they are not found in environment variables or the loaded .env files.
    LLM_KEY: Optional[str] = None
    LLM_MODEL: Optional[str] = None

    # --- Tool Configuration ---
    # Add API keys for any tools used
    TAVILY_API_KEY: str  # Required for Tavily search tool

    # --- Debugging ---
    # Optional setting with a default value.
    # Pydantic automatically converts "true"/"false", 1/0 to boolean.
    DEBUG: bool = False

    # --- Pydantic Model Configuration ---
    model_config = SettingsConfigDict(
        env_file=env_files_to_load,  # Tuple of .env files to load
        env_file_encoding="utf-8",  # Specify encoding for .env files
        case_sensitive=False,  # Match environment variables case-insensitively
        extra="ignore",  # Ignore extra variables found in the environment or .env files
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
        debug_config_dict["LLM_KEY"] = (
            "********" if debug_config_dict.get("LLM_KEY") else None
        )
        config_logger.debug(f"Configuration loaded successfully: {debug_config_dict}")
    else:
        config_logger.info("Configuration loaded successfully.")

except Exception as validation_error:
    # Catch any validation errors from Pydantic during instantiation
    config_logger.error(
        f"CRITICAL: Failed to load or validate application configuration. Error: {validation_error}",
        exc_info=True,
    )
    # Re-raise a more general error to halt execution if config is invalid
    raise ValueError(
        f"Configuration error - please check environment variables and .env files: {validation_error}"
    ) from validation_error
