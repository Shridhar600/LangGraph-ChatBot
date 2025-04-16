from langgraph.checkpoint.memory import InMemorySaver

def getInMemoryStore():
    return InMemorySaver()