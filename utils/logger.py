import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/data/bot.log'),
            logging.StreamHandler()
        ]
    )
    error_handler = logging.FileHandler('/data/error.log')
    error_handler.setLevel(logging.ERROR)
    logging.getLogger('').addHandler(error_handler)

    logging.info('Logging is configured.')
