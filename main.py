from typing import Annotated, TypedDict
from llmFactory import getLLMClient
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END, MessagesState
from utils.logger import logger


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm = getLLMClient().get_client()
if llm is None:
    raise ValueError("LLM client could not be initialized. Check your configuration.")

def chatbot(state: AgentState) -> dict:
    """ Returns the chatbot response."""
    try: 
        return {"messages": [llm.invoke(state['messages'])]}
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}")
        return {"messages": [{"role": "assistant", "content": "I encountered an error. Please try again."}]}


def getGraphWorkflow() -> StateGraph:
    """ Returns the graph workflow for the agent."""
    workflow = StateGraph(AgentState)

    workflow.add_node('chatbot',chatbot)
    workflow.add_edge(START, 'chatbot')
    workflow.add_edge('chatbot', END)

    return workflow


graph = getGraphWorkflow().compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [
        {"role": "user",
         "content": user_input}
        ]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


def main():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break


if __name__ == "__main__":
    main()