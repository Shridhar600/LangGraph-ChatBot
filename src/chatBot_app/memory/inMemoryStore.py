from langgraph.checkpoint.memory import InMemorySaver
from ..utils import setup_logger

log = setup_logger(__name__)


def get_in_memory_store():
    store = InMemorySaver()
    log.info("In-memory store created successfully.")
    return store
