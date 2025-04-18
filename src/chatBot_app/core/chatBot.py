class ChatBot:
    """A class to handle the chat bot functionality."""
    def __init__(self, compliedGraph):
        self.compliedGraph = compliedGraph
     
          
    def stream_graph_and_print_updates(self, user_input: str):
        """
        Streams updates from the provided graph for a given user input 
        and prints the assistant's responses to the console."""
        try:
            # Stream events from the graph
            for event in self.compliedGraph.stream({"messages": [
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
                            # logger.warning(f"CLI: Received message without 'content' attribute: {last_message}")
                            pass
                    else:
                        # Log if the event value doesn't contain expected messages
                        # logger.warning(f"CLI: Received event value in graph's stream without valid 'messages': {value}")
                        pass
        except Exception as e:
            # Log errors during streaming
            # logger.error(f"CLI: Error streaming graph updates: {str(e)}", exc_info=True)
            print("Assistant: Sorry, an error occurred while processing your request.")