from typing import Any


class CommonUtils:
    def isValidTool(toolsList: list, tool: Any) -> bool:
        if tool != None:
            toolsList.append(tool)
