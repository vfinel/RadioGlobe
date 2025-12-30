import logging
from logging.handlers import RotatingFileHandler

def get_logger():
    file_logger = RotatingFileHandler("logs/radioglobe.log", maxBytes=5e6, backupCount=1)
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.StreamHandler(), file_logger],
    )

    return file_logger 
