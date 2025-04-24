from typing import Any
from .logger import setup_logger

log = setup_logger(__name__)

class CommonUtils:
    
    @staticmethod
    def isValidTool(tool: Any ) -> bool:
        if tool is not None:
            return True
        else:
            log.warning("Tool %s is invalid and not added to the list.", tool.__class__.__name__)
            return False

