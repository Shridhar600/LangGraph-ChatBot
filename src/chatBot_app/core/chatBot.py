from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, AIMessage
from ..utils import setup_logger

log = setup_logger(__name__)


class ChatBot:
    """A class to handle the chat bot functionality."""

    def __init__(self, compliedGraph: CompiledStateGraph):
        if not isinstance(compliedGraph, CompiledStateGraph):
            raise Exception("Invalid graph object provided. Must be a CompiledGraph.")
        self.graph = compliedGraph

    def stream_graph(self, user_input: str, threadId: int):
        """
        Streams updates from the provided graph for a given user input
        and prints the assistant's responses to the console."""

        config = {"configurable": {"thread_id": threadId}}

        try:
            # Stream events from the graph
            for event in self.graph.stream(
                {"messages": [HumanMessage(content=user_input)]}, config=config
            ):
                # print(type(event)) #event is a dictionary, key is node's Name and the value is output of chatAgentNode which is {"messages":[response],"randomBullshit": "test" }
                # print(event)

                for node_output in event.values():  # using Values() cause we don't know what the key is going to be (node's name).
                    # print(type(node_output)) # value is also a dictionary and here is the state output by the node. Now, this dictionary is the output by the Node
                    # print(type(node_output["messages"]))
                    # print(node_output)
                    log.debug(f"Node output: {node_output}")
                    if (
                        isinstance(node_output["messages"][-1], AIMessage)
                        and node_output["messages"][-1].content
                        and node_output["messages"][-1].content.strip()
                    ):
                        print("Assistant: ", node_output["messages"][-1].content)

        except Exception:
            # Log errors during streaming
            # logger.error(f"CLI: Error streaming graph updates: {str(e)}", exc_info=True)
            print("Assistant: Sorry, an error occurred while processing your request.")


# --- Starting Conversation (Thread: cli_thread_0) ---
# User: hi
# <class 'langgraph.pregel.io.AddableUpdatesDict'>
# {'chatAgent': {'messages': [AIMessage(content='Hi there! How can I help you today?', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'xxxxx', 'safety_ratings': []}, id='xxxxx', usage_metadata={'input_tokens': 48, 'output_tokens': 11, 'total_tokens': 59, 'input_token_details': {'cache_read': 0}})], 'randomBullshit': 'test'}}
# <class 'dict'>
# <class 'list'>
# {'messages': [AIMessage(content='Hi there! How can I help you today?', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'xxxxx', 'safety_ratings': []}, id='xxxxx', usage_metadata={'input_tokens': 48, 'output_tokens': 11, 'total_tokens': 59, 'input_token_details': {'cache_read': 0}})], 'randomBullshit': 'test'}
# Assistant:  Hi there! How can I help you today?
# User:
