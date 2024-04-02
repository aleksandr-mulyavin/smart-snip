import os
import requests
import base64
import logging

from io import BytesIO
from PIL.Image import Image

from api_models import ImageToTextRequest, ImageToDataResponse, OCRData

API_METHOD_TO_TEXT = 'image_to_text'
"""Имя метода для распознавания текста на изображении"""

API_METHOD_TO_DATA = 'image_to_data'
"""Имя метода для распознавания блоков текста на изображении"""

__LOGGER = logging.getLogger(__name__)


def call_image_to_text(url: str, token: str, image: Image) -> str | None:
    """
    Вызов метода распознавания текста на изображении
    :param url: URL сервиса
    :param token: Токен авторизации
    :param image: Объект изображения (PIL.Image)
    :return: Распознанный текст
    """

    # Упаковка изображения в Base64
    image_base64 = __image_to_base64(image)

    # Заполнение структуры запроса
    request_data = ImageToTextRequest(
        image=image_base64)

    # Формирование заголовка запроса
    headers = __create_request_header(
        token=token)

    try:
        # Отправка запроса серверу API
        full_url = f'{url}{API_METHOD_TO_TEXT}'
        http_response = requests.post(
            full_url,
            headers=headers,
            json=request_data.model_dump(mode='json'))

        # Логирование ответа от сервера
        __LOGGER.log(
            level=logging.INFO,
            msg=f'{full_url} -> {http_response.status_code}'
                f': {http_response.text}')

        # Возврат пустого текста, если ошибка
        if http_response.status_code != requests.codes.ok:
            return None

        # Обработка положительного ответа сервера
        text = http_response.text
        if not len(text):
            return text

        # Удаление из текста ковычек и замена переносов строк
        text = text.replace('\\n', os.linesep)
        text = text[1:]
        text = text[:-1]
        if text[:-2] == os.linesep:
            text = text[:-1]
        return text
    except Exception as e:
        __LOGGER.exception(e)
        return None


def call_image_to_data(url: str, token: str, image: Image) -> list[OCRData]:
    """
    Вызов метода распознавания блоков текста на изображении
    :param url: URL сервиса
    :param token: Токен авторизации
    :param image: Объект изображения (PIL.Image)
    :return: Список распознанных блоков на изображении
    """

    # Упаковка изображения в Base64
    image_base64 = __image_to_base64(image)

    # Заполнение структуры запроса
    request_data = ImageToTextRequest(
        image=image_base64)

    # Формирование заголовка запроса
    headers = __create_request_header(
        token=token)

    try:
        # Отправка запроса серверу API
        full_url = f'{url}{API_METHOD_TO_TEXT}'
        http_response = requests.post(
            full_url,
            headers=headers,
            json=request_data.model_dump(mode='json'))

        # Логирование ответа от сервера
        __LOGGER.log(
            level=logging.INFO,
            msg=f'{full_url} -> {http_response.status_code}'
                f': {http_response.text}')

        # Возврат пустого списка, если ошибка
        if http_response.status_code != requests.codes.ok:
            return []

        # Обработка положительного ответа сервера
        image_data_response = ImageToDataResponse(**http_response.json())
        return image_data_response.image_data
    except Exception as e:
        __LOGGER.exception(e)
        return []


def __image_to_base64(image: Image) -> bytes:
    """
    Функция упаковки изображения в Base64
    :param image: Объект изображения (PIL.Image)
    :return: Base64
    """
    io_buffer = BytesIO()
    image.save(io_buffer, format="JPEG")
    return base64.b64encode(io_buffer.getvalue())


def __create_request_header(token: str) -> dict:
    """
    Функция формирования заголовка запроса
    :param token: Токен авторизации
    :return: Словарь заголовка
    """
    return {'X-API-key': token,
            'Content-Type': 'application/json'}
