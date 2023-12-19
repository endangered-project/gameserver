import logging


def get_logger_with_name(name: str) -> logging.Logger:
    """
    Get a logger with the given name
    :param name: Name of the logger
    :return: Logger
    """
    logger = logging.getLogger(name)
    return logger


def get_logger() -> logging.Logger:
    """
    Get a logger with the name of the caller
    :return: Logger
    """
    logger = logging.getLogger(__name__)
    return logger
