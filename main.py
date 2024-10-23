import logging
import os
import sys
from src.interfaces.console.cli import CLI
from dotenv import load_dotenv


def setup_logging():

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), 'resources', '.env')
    load_dotenv(dotenv_path)

    # Get log level from environment variable
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging initialized with level: {log_level}")


def main():
    setup_logging()
    cli = CLI()
    try:
        cli.run()
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        print("An unexpected error occurred. Please check the logs for more details.")


if __name__ == "__main__":
    main()
