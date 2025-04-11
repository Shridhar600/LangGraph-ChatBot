from graph.workflow import graph_instance
from utils.logger import logger

def stream_graph_and_print_updates(graph, user_input: str):
    """
    Streams updates from the provided graph for a given user input 
    and prints the assistant's responses to the console."""
    try:
        # Stream events from the graph
        for event in graph.stream({"messages": [
            {"role": "user", "content": user_input}
        ]}):
            # Process each event in the stream
            for value in event.values():
                # Check if the event value contains messages
                if value.get("messages") and isinstance(value["messages"], list) and value["messages"]:
                    # Get the last message (usually the assistant's response)
                    last_message = value["messages"][-1]
                    # Ensure the message has content before printing
                    if hasattr(last_message, 'content'):
                        print(f"Assistant: {last_message.content}")
                    else:
                        logger.warning(f"CLI: Received message without 'content' attribute: {last_message}")
                else:
                    # Log if the event value doesn't contain expected messages
                    logger.warning(f"CLI: Received event value in graph's stream without valid 'messages': {value}")
    except Exception as e:
        # Log errors during streaming
        logger.error(f"CLI: Error streaming graph updates: {str(e)}", exc_info=True)
        print("Assistant: Sorry, an error occurred while processing your request.")

def start_cli():
    """ Starts the command-line interface loop for interacting with the chatbot."""

    print("Chatbot initialized. Type 'quit', 'exit', or 'q' to end.")
    while True:
        try:
            user_input = input("User: ") # User Input
            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            # Stream the graph and print updates for the user's input
            stream_graph_and_print_updates(graph_instance, user_input)

        except EOFError: # Handle Ctrl+D or end of input stream
             print("\nGoodbye!")
             break
        except KeyboardInterrupt: # Handle Ctrl+C
             print("\nInterrupted. Goodbye!")
             break
        except Exception as e:
            # Log unexpected errors in the main loop
            logger.error(f"CLI: Error in main loop: {str(e)}", exc_info=True)
            print("An unexpected error occurred. Exiting.")
            break
