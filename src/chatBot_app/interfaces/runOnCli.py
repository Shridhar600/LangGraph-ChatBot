import sys # For sys.exit
from ..core import ChatBot
from ..llmModels import create_llm_client
from ..graphs import create_simple_graph
from ..memory import get_in_memory_store
from ..tools import get_tools
from ..utils import setup_logger, CHATBOT_SYSTEM_PROMPT # create_graph_mermaid_png removed as it's commented out
from ..utils.exceptions import (
    LLMAPIError, ToolExecutionError, GraphError, AppException,
    LLMInitializationError, ToolInitializationError, ConfigurationError,
    InvalidStateError, EmbeddingError, VectorStoreError, DocumentLoadingError
)
from src.rag_app.core import rag_setup # Import rag_setup

log = setup_logger(__name__)

def start_cli():
    """Starts the command-line interface loop for interacting with the chatbot."""

    try:
        log.info("Initializing RAG setup...")
        rag_setup() # Explicitly call rag_setup
        log.info("RAG setup completed successfully.")

        log.info("Loading tools...")
        tools = get_tools()
        log.info("Tools loaded.")

        log.info("Creating LLM client...")
        chatAgent = create_llm_client(tools=tools, isToolsEnabled=True)
        log.info("LLM client created.")

        log.info("Initializing memory store...")
        memory = get_in_memory_store()
        log.info("Memory store initialized.")

        log.info("Creating graph...")
        graph = create_simple_graph(chatAgent, memory, tools, CHATBOT_SYSTEM_PROMPT)
        log.info("Graph created.")

        log.info("Initializing ChatBot...")
        chatbot = ChatBot(graph)
        log.info("ChatBot initialized.")

        # create_graph_mermaid_png(graph) # Still commented out

    except ConfigurationError as e:
        log.critical(f"Configuration Error during setup: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Configuration failed: {e}. Please check your environment variables and .env files. Exiting.")
        return # Or sys.exit(1)
    except DocumentLoadingError as e:
        log.critical(f"Document Loading Error during RAG setup: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to load documents for RAG: {e}. Exiting.")
        return
    except EmbeddingError as e:
        log.critical(f"Embedding Error during RAG setup: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to initialize embedding model for RAG: {e}. Exiting.")
        return
    except VectorStoreError as e:
        log.critical(f"Vector Store Error during RAG setup or tool use: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Vector store operation failed: {e}. Exiting.")
        return
    except ToolInitializationError as e:
        log.critical(f"Tool Initialization Error during setup: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to initialize tools: {e}. Exiting.")
        return
    except LLMInitializationError as e:
        log.critical(f"LLM Initialization Error during setup: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to initialize LLM: {e}. Exiting.")
        return
    except (GraphError, InvalidStateError) as e: # Catching InvalidStateError specifically for graph or ChatBot init
        log.critical(f"Graph or ChatBot Initialization Error: {e}", exc_info=True)
        print(f"CRITICAL ERROR: Failed to initialize chat graph or chatbot: {e}. Exiting.")
        return
    except AppException as e: # Catch-all for other app-specific critical setup errors
        log.critical(f"Application Error during setup: {e}", exc_info=True)
        print(f"CRITICAL APPLICATION ERROR: {e}. Exiting.")
        return
    except Exception as e: # Catch any other unexpected critical setup error
        log.critical(f"Unexpected critical error during setup: {e}", exc_info=True)
        print(f"CRITICAL UNEXPECTED ERROR: {e}. Exiting.")
        return

    print( "\nChatbot initialized successfully. Type 'quit', 'exit', or 'q' to end or 'new' to start a new conversation thread."
    )

    thread_id_counter = 0
    current_thread_id = f"cli_thread_{thread_id_counter}"
    print(f"\n--- Starting Conversation (Thread: {current_thread_id}) ---")

    while True:
        try:
            user_input = input("User: ")  # User Input
            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print(f"Exiting chat thread {current_thread_id}.")
                print("Goodbye!")
                break
            if user_input.lower() == "new":
                thread_id_counter += 1
                current_thread_id = f"cli_thread_{thread_id_counter}"
                print(f"Starting new conversation thread: {current_thread_id}")
                continue

            if not user_input.strip():
                print("User input is empty. Please enter a valid message.")
                continue

            response  =  chatbot.stream_graph(
                user_input, current_thread_id
            )  # Pass user input to the chatbot
            if response:
                for message in response:
                    if isinstance(message, str):
                        print("Assistant:", message) # Added colon for consistency
                    else:
                        log.warning(f"Assistant: Received non-string message part: {type(message)}")
                        
        except EOFError:
            print("\nExiting Chatbot (EOF). Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nExiting Chatbot (Interrupted by user). Goodbye!")
            break
        except LLMAPIError as e:
            log.error(f"LLM API Error during interaction: {e}", exc_info=True)
            print(f"Error: An issue occurred with the Language Model API: {e}")
        except ToolExecutionError as e:
            log.error(f"Tool Execution Error during interaction: {e}", exc_info=True)
            print(f"Error: An issue occurred while executing a tool: {e}")
        except GraphError as e:
            log.error(f"Graph Execution Error during interaction: {e}", exc_info=True)
            print(f"Error: An issue occurred within the chat graph execution: {e}")
        except InvalidStateError as e: # e.g. if chatbot somehow gets into a bad state mid-conversation
            log.error(f"Invalid State Error during interaction: {e}", exc_info=True)
            print(f"Error: The application encountered an invalid state: {e}")
        except AppException as e: # Catch-all for other app-specific errors
            log.error(f"Application Error during interaction: {e}", exc_info=True)
            print(f"Error: An application error occurred: {e}")
        except Exception as e:
            log.critical(f"An unexpected error occurred during interaction: {e}", exc_info=True)
            print(f"CRITICAL UNEXPECTED ERROR: {e}. Please report this issue or try starting a new conversation.")
            # Depending on severity, could break here or let user decide if they want to continue.
            # For a CLI, often good to break on truly unexpected issues.
            # However, the prompt implies the loop should generally continue.
            # For now, will let it continue as per "loop should generally continue".

