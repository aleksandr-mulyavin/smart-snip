"""
Описание структур запросов и ответов сервисов
Скопировано из модулей api_server/src/domain
"""
from pydantic import BaseModel


class ImageToTextRequest(BaseModel):
    """
    Структура запроса метода распознавания текста
    на изображении ImageToText
    """

    image: str
    """Изображение в Base64"""

    lang: str = ''
    """Язык текста (опционально)"""


class OCRData(BaseModel):
    """
    Структура данных о распознанном блоке текста
    """

    level: int
    """Уровень блока"""
    page_num: int
    """Номер страницы"""
    block_num: int
    """Номер блока"""
    par_num: int
    """Номер параграфа"""
    line_num: int
    """Номер строки"""
    word_num: int
    """Количество слов"""
    left: int
    """Отступ слева"""
    top: int
    """Отступ сверху"""
    width: int
    """Ширина блока"""
    height: int
    """Высота блока"""
    conf: float
    """Коэффициент достоверности"""
    text: str
    """Текст"""


class ImageToDataResponse(BaseModel):
    """
    Структура ответа метода распознавания текста
    на изображении ImageToText
    """

    image_data: list[OCRData]
    """Список распознанных блоков на изображении"""


class TranslateImageTextRequest(BaseModel):
    """
    Структура запроса метода перевода текста
    на изображении TranslateImageText
    """

    image: str
    """Изображение в Base64"""
    to_lang: str = ''
    """Целевой язык перевода (опционально)"""


class TranslateImageTextResponse(BaseModel):
    """
    Структура ответа метода перевода текста
    на изображении TranslateImageText
    """
    image: str
    """Изображение в Base64 с переведенным текстом"""


class Error(BaseModel):
    """
    Структура ошибки сервисов
    """

    error: str
    """Текст ошибки"""
