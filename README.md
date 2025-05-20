# LangGraph Chatbot Project

## Description

This project implements a conversational chatbot using the LangChain and LangGraph libraries. It features a modular and extensible architecture, incorporating various components like tools, memory, and prompt templates to enhance the chatbot's capabilities. The project supports different interfaces, including a Command Line Interface (CLI) and a Streamlit web application with user authentication. It also integrates a Retrieval-Augmented Generation (RAG) system to enhance the chatbot's knowledge and response generation.

## Features

*   Conversational chatbot interface via Command Line (CLI) and Streamlit web app with user authentication.
*   Modular design with clear separation of concerns.
*   Integration of various tools to extend chatbot functionality (e.g., human assistance, web search, RAG).
*   Implementation of memory for maintaining conversation history.
*   Utilizes prompt templates for flexible and dynamic prompt generation.
*   Configurable LLM provider with support for different models (e.g., Gemini, OpenAI, Ollama).
*   Configuration loaded from `.env` files.
*   Includes logging for monitoring and debugging.
*   Retrieval-Augmented Generation (RAG) system for enhanced knowledge retrieval.
*   Streamlit UI with login page and dummy accounts.

## Project Structure

```
.
├── .env                  # Environment variables (API keys, etc.) - REQUIRED
├── .gitignore            # Git ignore file
├── main.py               # Main application entry point for CLI
├── README.md             # Project README file
├── requirements.txt      # Project dependencies
├── streamlitApp.py       # Streamlit web application entry point
└── src/
    └── chatBot_app/
        ├── __init__.py
        ├── config.py         # Configuration loading and validation
        ├── core/
        │   ├── __init__.py
        │   └── chatBot.py    # Core chatbot logic
        ├── exceptions/       # Custom exceptions for handling specific errors
        │   └── __init__.py
        ├── graphs/
        │   ├── __init__.py
        │   └── simpleChatBotGraph.py # LangGraph workflow definition
        ├── graphStates/
        │   ├── __init__.py
        │   └── agentState.py # Agent state definition
        │   └── rag_agent_state.py # Agent state for RAG-based conversations
        ├── interfaces/
        │   ├── __init__.py
        │   └── runOnCli.py   # Command Line Interface implementation
        ├── llmModels/        # LLM client handling
        │   ├── __init__.py
        │   ├── baseLlmModel.py # Abstract base class for LLM clients
        │   ├── chatGemini.py # Google Gemini client implementation
        │   ├── chatOpenAI.py # OpenAI client implementation
        │   ├── chat_ollama.py # Ollama client implementation
        │   └── llmFactory.py # Factory for creating LLM client instances
        ├── memory/           # Conversation memory
        │   ├── __init__.py
        │   └── inMemoryStore.py # In-memory memory implementation
        ├── nodes/            # LangGraph node definitions
        │   ├── __init__.py
        │   └── chatAgentNode.py # Agent node
        │   └── toolsNode.py  # Tools node
        ├── tools/            # Integrated tools
        │   ├── __init__.py
        │   ├── human_assistance.py # Human assistance tool
        │   ├── rag_tool.py      # Tool for interacting with the RAG system
        │   ├── tavilyWebSearchTool.py # Tavily web search tool
        │   └── toolsRegistry.py # Tool registration and management
        └── utils/            # Utility functions and classes
            ├── __init__.py
            ├── commonUtils.py # Common utility functions
            ├── get_current_system_details.py # Utility to fetch current system details
            ├── graphMermaidDiagram.py # Utility for generating graph diagrams
            ├── logger.py         # Logging setup
            ├── prompt_template.py # Prompt template handling
            └── prompts.py        # Prompt definitions
    └── rag_app/
        ├── __inti__.py
        ├── core/
        │   ├── __init__.py
        │   ├── rag_setup.py   # RAG setup logic
        │   └── vector_store_singleton.py # Singleton for vector store
        ├── document_loaders/ # Document loaders
        │   ├── __init__.py
        │   └── web_loader.py  # Web page loader
        ├── embedding_models/ # Embedding models
        │   ├── __init__.py
        │   ├── embed_model_factory.py # Factory for embedding models
        │   └── ollama_embed.py # Ollama embedding model
        ├── retriever/        # Retriever logic
        │   ├── __init__.py
        │   └── similarity_search.py # Similarity search retriever
        ├── splitters/        # Text splitters
        │   ├── __init__.py
        │   └── recursive_text_splitter.py # Recursive text splitter
        └── vector_store/     # Vector store
            ├── __init__.py
            ├── vector_store.py # Vector store interface
            ├── vector_store_factory.py # Factory for vector stores

```

## Setup and Installation

1.  **Clone the repository:**
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
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Environment File (`.env`):**
    Create a file named `.env` in the project root directory and add the necessary configuration variables (see Configuration section below). This file is crucial for API keys and model settings.

## Configuration

Configuration is managed via environment variables and `.env` files, loaded by `src/chatBot_app/config.py`.

**Required `.env` variables:**

*   `LLM_PROVIDER`: The LLM provider to use (e.g., `gemini`, `openai`, `ollama`).
*   `LLM_KEY`: Your API key for the chosen LLM provider (if required).
*   `LLM_MODEL`: The specific model name for the chosen provider (e.g., `gemini-pro`, `gpt-4o`, `llama2`).
*   `TAVILY_API_KEY`: Your API key for the Tavily web search tool.

**Optional `.env` variables:**

*   `DEBUG`: Set to `true` to enable debug logging. Defaults to `false`.

**Example `.env` file:**

```dotenv
# .env
LLM_PROVIDER=gemini
LLM_KEY=YOUR_LLM_API_KEY_HERE
LLM_MODEL=gemini-pro
TAVILY_API_KEY=YOUR_TAVILY_API_KEY_HERE
DEBUG=false
```

## Usage

### Command Line Interface (CLI)

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Make sure your `.env` file is correctly configured with your API keys and desired models.
3.  Run the CLI application from the project root directory:

    ```bash
    python main.py
    ```

4.  Interact with the chatbot in your terminal. Type `quit`, `exit`, or `q` to stop.

### Streamlit Web Application

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Make sure your `.env` file is correctly configured with your API keys and desired models.
3.  Run the Streamlit application from the project root directory:

    ```bash
    streamlit run streamlitApp.py
    ```

4.  The Streamlit app will open in your web browser.
5.  Use the following credentials to log in to the dummy account:
    *   **Username:** admin
    *   **Password:** admin123
    *   **Username:** demo
    *   **Password:** demo123

## Extending the Project

*   **Adding new LLM providers:** Create a new class in `src/chatBot_app/llmModels/` that inherits from `BaseLlmModel` and implement the required methods. Add the new provider to the `LlmFactory`.
*   **Adding new tools:** Create a new tool function or class and register it in `src/chatBot_app/tools/toolsRegistry.py`.
*   **Modifying the graph:** Adjust the workflow and nodes in `src/chatBot_app/graphs/simpleChatBotGraph.py` to change the chatbot's behavior.
*   **Implementing different memory types:** Create a new memory class in `src/chatBot_app/memory/` that adheres to a defined interface and update the chatbot to use it.
*   **Integrating new data sources for RAG:** Implement a new document loader in `src/rag_app/document_loaders/` and update the RAG setup to use it.
