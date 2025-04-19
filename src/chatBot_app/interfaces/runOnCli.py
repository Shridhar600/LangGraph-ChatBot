from chatBot_app.core import ChatBot
from chatBot_app.llmModels import create_llm_client
from chatBot_app.graphs import create_simple_graph
from chatBot_app.memory import getInMemoryStore


def start_cli():
    """ Starts the command-line interface loop for interacting with the chatbot."""

    chatModel = create_llm_client()
    memory = getInMemoryStore()
    graph = create_simple_graph(chatModel,memory)
    chatbot = ChatBot(graph) 

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

            response = chatbot.stream_graph(user_input, current_thread_id) # Pass user input to the chatbot
            if response:
                print(f"Assistant: {response}")
            else:
                print("Assistant: No response received. Please try again.")
                
        except EOFError: # Handle Ctrl+D or end of input stream
             print("\nGoodbye!")
             break
        except KeyboardInterrupt: # Handle Ctrl+C
             print("\nInterrupted. Goodbye!")
             break
        except Exception as e:
            # Log unexpected errors in the main loop
            # logger.error(f"CLI: Error in main loop: {str(e)}", exc_info=True)
            print(f"An unexpected error occurred: {e}") # Print the specific error
            break
