from ..core import ChatBot
from ..llmModels import create_llm_client
from ..graphs import create_simple_graph
from ..memory import get_in_memory_store
from ..tools import get_tools
from ..utils import setup_logger, create_graph_mermaid_png


log = setup_logger(__name__)


def start_cli():
    """ Starts the command-line interface loop for interacting with the chatbot."""

    tools = get_tools()    
    chatAgent = create_llm_client(tools=tools, isToolsEnabled=True)
    memory = get_in_memory_store()
    graph = create_simple_graph(chatAgent, memory, tools)
    chatbot = ChatBot(graph) 

    create_graph_mermaid_png(graph)

    print("Chatbot initialized. Type 'quit', 'exit', or 'q' to end or 'new' to start a new conversation thread.")

    thread_id_counter = 0
    current_thread_id = f"cli_thread_{thread_id_counter}"
    print(f"\n--- Starting Conversation (Thread: {current_thread_id}) ---")
    
    while True:
        try:
            user_input = input("User: ") # User Input
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

            chatbot.stream_graph(user_input, current_thread_id) # Pass user input to the chatbot
                
        except EOFError: # Handle Ctrl+D or end of input stream
             print("\nGoodbye!")
             break
        except KeyboardInterrupt: # Handle Ctrl+C
             print("\nInterrupted. Goodbye!")
             break
        except Exception as e:
            log.error(f"An unexpected error occurred: {e}")
            break