from typing import Any
from langgraph.prebuilt import ToolNode


def get_tools_node(tools: list) -> ToolNode:
    return ToolNode(tools=tools)