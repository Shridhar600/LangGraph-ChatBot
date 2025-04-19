from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage


class ChatBot:
    """A class to handle the chat bot functionality."""
    def __init__(self, compliedGraph: CompiledStateGraph):
        if not isinstance(compliedGraph, CompiledStateGraph):
            raise Exception("Invalid graph object provided. Must be a CompiledGraph.")        
        self.graph = compliedGraph

          
    def stream_graph(self, user_input: str, threadId:int) -> str:
        """
        Streams updates from the provided graph for a given user input 
        and prints the assistant's responses to the console."""
        config = {"configurable": {"thread_id": threadId}}
        try:
            # Stream events from the graph
            for event in self.graph.stream({"messages": [HumanMessage(content=user_input)]},config=config):
                # Process each event in the stream
                for value in event.values():
                    # Check if the event value contains messages
                    if value.get("messages") and isinstance(value["messages"], list) and value["messages"] is not None:
                        # Get the last message from the list (usually the assistant's response)
                        last_message: list = value["messages"][-1]
                        # Ensure the message has content before printing
                        if hasattr(last_message, 'content'):
                            # print(f"Assistant: {last_message.content}")
                            return last_message.content
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