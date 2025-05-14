from . import setup_logger

log = setup_logger(__name__)


def create_graph_mermaid_png(graph):
    try:
        # Save the PNG image to a file
        graph_image = graph.get_graph().draw_mermaid_png()
        with open("graph_output.png", "wb") as f:
            f.write(graph_image)
        log.info("Graph saved as 'graph_output.png'.")
    except Exception as e:
        log.error(f"An error occurred while saving the graph: {e}")
        raise e
