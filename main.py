from utils.logger import logger 
from interfaces.cli import start_cli

if __name__ == "__main__":
    logger.info("Application starting...")
    # Start the Command Line Interface
    start_cli()
    logger.info("Application finished.")
