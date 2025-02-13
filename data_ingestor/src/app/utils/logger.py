# app/utils/logger.py
import logging

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with a standard format.
    Ensures that multiple calls do not add duplicate handlers.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
