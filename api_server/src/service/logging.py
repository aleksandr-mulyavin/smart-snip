import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str) -> logging.Logger:
    """Возвращает объект логера с переданным именем.

    Параметры:
        name (str): имя логера

    Возвращаемое значение:
        logging.Logger: объект логера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_handler = TimedRotatingFileHandler(
        f"logs/{name}.log", encoding='utf-8', when='D'
    )
    log_formatter = logging.Formatter(
        u"%(name)s %(asctime)s %(levelname)s %(message)s"
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger
