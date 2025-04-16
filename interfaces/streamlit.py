from utils import logger


def stream_graph_and_get_response(graph, user_input: str,config) -> str:
    """
    Streams updates from the provided graph for a given user input 
    and returns the assistant's response as a string."""
    response_text = ""
    try:
        for event in graph.stream({"messages": [
            {"role": "user", "content": user_input}
        ]},config):
            for value in event.values():
                if value.get("messages") and isinstance(value["messages"], list) and value["messages"]:
                    last_message = value["messages"][-1]
                    if hasattr(last_message, 'content'):
                        response_text = last_message.content
    except Exception as e:
        logger.error(f"Streamlit: Error streaming graph updates: {str(e)}", exc_info=True)
        response_text = "Sorry, an error occurred while processing your request."

    return response_text
    