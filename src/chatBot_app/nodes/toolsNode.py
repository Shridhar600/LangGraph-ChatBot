import json
from langchain_core.messages import ToolMessage
from langgraph.graph import END
from ..utils import setup_logger

log = setup_logger(__name__)


# Unused in this project but, gives an idea of how to use to create a Tool Node for the llm to use in the graph. 

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict): #This makes the class callable, so we can use it like a function.
        """Run the tools requested in the last AIMessage."""
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
          #here we are checking if tools available in this node and the tool called by the llm match or not.
          # tool.invoke("What's a 'node' in LangGraph?") is what is happening here. we are invoking the tavilySearch by passing the args requested by the LLM.

            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(  # Here we created a ToolMessage type object which contains the name of the Tool to be called from the LLM which we assigned to the llm using bindTools. This will pass the name of the tool and the arguments required to run it.

                # Like here we are the LLM with have a tool_calls property in the response (AiMessage) from which we are extracting the tool name.

                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs} # Output is a list of ToolMessage objects. This Will contain content, of all the tools called in the last message.    
    
# //********* Example of how to use this node in a graph **********/    
# tool_node = BasicToolNode(tools=[tool])
# graphWithWebSearch.add_node("tools", tool_node)


def route_tools(state: any) -> str:
    """
    Provide this function to the graph by calling add_conditional_edges, 
    which tells the graph that whenever the chatbot node completes to check this function to see where to go next. 
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
    # Basically, checking if state is a list. For Traversal.
        ai_message = state[-1]
    elif messages := state.get("messages", []):
      #Negative Indexing:
      # Negative indexing means start from the end
      # -1 refers to the last item, -2 refers to the second last item etc.
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0: #Check if the last message has tool calls and also check if the tool calls are not empty.
        return "tools"
    return END

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.

# graphWithWebSearch.add_conditional_edges(
#     "chatbotWithTool",
#     route_tools,
#     # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
#     # It defaults to the identity function, but if you
#     # want to use a node named something else apart from "tools",
#     # You can update the value of the dictionary to something else
#     # e.g., "tools": "my_tools"
#     {"tools": "tools", END: END},
# )

