from hashlib import md5


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
