"""
Logging
-------
Description.
"""

import logging


def get_logger(name: str, level: int = 20):
    """
    Logger builder. Returns logger with given name and level.

    Parameters
    ----------
    name : str
        The name of the logger.
    level : int
        See levels in logging.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(f"logs/{name}.log", mode='w')
    formatter = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
