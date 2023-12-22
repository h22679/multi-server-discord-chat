import logging
import os

# Define the path to the data directory relative to the location of logger.py
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Create the data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Define paths for the log files
BOT_LOG_FILE = os.path.join(DATA_DIR, 'bot.log')
ERROR_LOG_FILE = os.path.join(DATA_DIR, 'error.log')

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(BOT_LOG_FILE),
            logging.StreamHandler()
        ]
    )
    error_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_handler.setLevel(logging.ERROR)
    logging.getLogger('').addHandler(error_handler)

    logging.info('Logging is configured.')