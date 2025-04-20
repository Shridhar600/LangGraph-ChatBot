import logging
from .. import Config

def setup_logger(module_name: str):
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

        logger.addHandler(handler)
        # logger.propagate = False  # prevents duplicate logs in some cases

    return logger
