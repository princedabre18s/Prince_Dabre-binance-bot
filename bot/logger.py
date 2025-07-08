# Logging setup and utilities
import logging

def setup_logger():
    logging.basicConfig(
        filename='bot.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
