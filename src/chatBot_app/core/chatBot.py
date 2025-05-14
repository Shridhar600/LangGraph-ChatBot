from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import interrupt, Command, Interrupt

from ..utils import setup_logger

log = setup_logger(__name__)


class ChatBot:
    """A class to handle the chat bot functionality."""

    def __init__(self, compliedGraph: CompiledStateGraph):
        if not isinstance(compliedGraph, CompiledStateGraph):
            raise Exception("Invalid graph object provided. Must be a CompiledGraph.")
        self.graph = compliedGraph

    def stream_graph(self, user_input: str, threadId: int) -> list:
        """
        Streams updates from the provided graph for a given user input
        and prints the assistant's responses to the console."""

        config = {"configurable": {"thread_id": threadId}}
        response = []

        try:
            # Stream events from the graph
            for event in self.graph.stream(
                {"messages": [HumanMessage(content=user_input)],
                 "agentName": "Chhota Don"}, config=config
            ):
                #event is a dictionary, key is node's Name and the value is output of chatAgentNode which is {"messages":[response],"randomBullshit": "test" }
                for node_output in event.values():  # using Values() cause we don't know what the key is going to be (node's name).
                    # node_output is also a dictionary and here is the state output by the node. Now, this dictionary is the output by the Node
                    log.debug(f"Node output: {node_output}")
                    if (
                        isinstance(node_output["messages"][-1], AIMessage)
                        and node_output["messages"][-1].content
                        and node_output["messages"][-1].content.strip()
                    ):
                        response.append(node_output["messages"][-1].content)
                    if (hasattr((node_output["messages"][-1]), 'tool_calls') and node_output["messages"][-1].tool_calls):
                        log.info(f"LLM initiated a {[ tool_name['name'] for tool_name in ((node_output['messages'][-1]).tool_calls)]} Tool Call.")
                        
        except Exception as e:
            log.error(f"CLI: Error streaming graph updates: {str(e)}", exc_info=True)

        return response
    


########################################################

# Example of output from the graph: 
# Graph event: {'chatAgent': {'messages': [AIMessage(content='', additional_kwargs={'function_call': {'name': 'human_assistance', 'arguments': '{"query": "The user wants to build an agent."}'}}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.0-flash', 'safety_ratings': []}, id='run-fdf6cf7b-268d-4025-938a-62a5afa1d4bf-0', tool_calls=[{'name': 'human_assistance', 'args': {'query': 'The user wants to build an agent.'}, 'id': 'ed2a9239-15a1-4649-b5f2-5e24b4356766', 'type': 'tool_call'}], usage_metadata={'input_tokens': 78, 'output_tokens': 12, 'total_tokens': 90, 'input_token_details': {'cache_read': 0}})], 'randomBullshit': 'test'}}

# Node output: {'messages': [AIMessage(content='', additional_kwargs={'function_call': {'name': 'human_assistance', 'arguments': '{"query": "The user wants to build an agent."}'}}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.0-flash', 'safety_ratings': []}, id='run-fdf6cf7b-268d-4025-938a-62a5afa1d4bf-0', tool_calls=[{'name': 'human_assistance', 'args': {'query': 'The user wants to build an agent.'}, 'id': 'ed2a9239-15a1-4649-b5f2-5e24b4356766', 'type': 'tool_call'}], usage_metadata={'input_tokens': 78, 'output_tokens': 12, 'total_tokens': 90, 'input_token_details': {'cache_read': 0}})], 'randomBullshit': 'test'}