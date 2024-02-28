import logging
import os
from hashlib import md5
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


def check_token(token: str) -> bool:
    """Функция проверяет наличие хэш-суммы токена в списке разрешенных.

    Параметры:
        token (bytes): токен

    Возвращаемое значение:
        None.
    """
    token_md5 = md5(token.encode('utf-8')).hexdigest()

    try:
        with open('secrets.txt', 'r') as file:
            hash = file.readline().strip()
            if hash == token_md5:
                return True
    except FileNotFoundError:
        return False

    return False
