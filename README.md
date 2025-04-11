# LangGraph Chatbot Project

## Description

This project implements a basic chatbot using the LangChain and LangGraph libraries. It demonstrates a modular structure designed for clarity, maintainability, and future expansion. The chatbot interacts with a Large Language Model (LLM) based on the configured provider (currently supporting Google Gemini).

## Features

*   Basic conversational chatbot interface via Command Line (CLI).
*   Modular design separating concerns:
    *   Graph definition (`graph/`)
    *   Agent logic (`agents/`)
    *   LLM client handling (`llm_clients/`)
    *   Configuration (`settings/`)
    *   User interface (`interfaces/`)
    *   Utilities (`utils/`)
*   Configuration loaded from `.env` files using Pydantic for validation.
*   Support for different environments (Development/Production) via `ENV` variable and `.env.production` file.
*   Extensible LLM client factory (`llmFactory.py`) to easily add support for more providers.

## Project Structure

```
.
├── .env                  # Base environment variables (API keys, etc.) - REQUIRED
├── .env.production       # Optional overrides for production environment
├── .gitignore            # Git ignore file
├── main.py               # Main application entry point
├── llmFactory.py         # Factory for creating LLM client instances
├── agents/
│   └── chat_agent.py     # Core logic for LLM interaction
├── graph/
│   ├── nodes.py          # LangGraph node definitions
│   ├── state.py          # LangGraph state definition (AgentState)
│   └── workflow.py       # LangGraph workflow definition and compilation
├── interfaces/
│   └── cli.py            # Command Line Interface implementation
├── llm_clients/
│   ├── base.py           # Abstract base class for LLM clients
│   └── gemini.py         # Google Gemini client implementation
├── settings/
│   └── config.py         # Pydantic-based configuration loading and validation
└── utils/
    └── logger.py         # Logging setup
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    # Activate the environment
    # Windows (cmd.exe):
    venv\Scripts\activate
    # Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # macOS/Linux:
    source venv/bin/activate 
    ```

3.  **Install dependencies:**
    *(Assuming a requirements.txt file exists or will be created)*
    ```bash
    pip install -r requirements.txt 
    ```
    *If `requirements.txt` doesn't exist, you'll need to install manually:*
    ```bash
    pip install langchain langgraph langchain-google-genai python-dotenv pydantic pydantic-settings
    ```

4.  **Create Environment File (`.env`):**
    Create a file named `.env` in the project root directory and add the necessary configuration variables (see Configuration section below). This file is crucial for API keys and model settings.

## Configuration

Configuration is managed via environment variables and `.env` files, loaded by `settings/config.py` using Pydantic.

**Required `.env` variables:**

*   `LLM_PROVIDER`: The LLM provider to use. Currently supported: `gemini`. (Case-insensitive)
*   `LLM_KEY`: Your API key for the chosen LLM provider.
*   `LLM_MODEL`: The specific model name for the chosen provider (e.g., `gemini-pro`).

**Optional `.env` variables:**

*   `ENV`: Set the environment. Defaults to `dev`. Set to `prod` to load `.env.production` overrides.
*   `DEBUG`: Set to `true` to enable debug logging. Defaults to `false`.

**Example `.env` file:**

```dotenv
# .env
LLM_PROVIDER=gemini
LLM_KEY=YOUR_GEMINI_API_KEY_HERE 
LLM_MODEL=gemini-pro
DEBUG=false
ENV=dev 
```

**Example `.env.production` file (Optional Overrides):**

```dotenv
# .env.production
DEBUG=false
# Potentially override other settings for production if needed
```

## Usage

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Make sure your `.env` file is correctly configured with your API key and desired model.
3.  Run the application from the project root directory:

    ```bash
    python main.py
    ```

4.  Interact with the chatbot in your terminal. Type `quit`, `exit`, or `q` to stop.

## Future Improvements

*   Implement Dependency Injection for better testability and decoupling.
*   Add support for more LLM providers (e.g., OpenAI) by creating new client classes in `llm_clients/` and updating the registry in `llmFactory.py`.
*   Develop alternative interfaces (e.g., a web API using FastAPI).
*   Add more complex agent logic (e.g., tool usage, memory management).
*   Implement comprehensive unit and integration tests.
*   Generate a `requirements.txt` file.
