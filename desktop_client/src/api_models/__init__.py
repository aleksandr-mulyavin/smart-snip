from pydantic import BaseModel


class ImageToTextRequest(BaseModel):
    image: str
    lang: str = ''


class OCRData(BaseModel):
    level: int
    page_num: int
    block_num: int
    par_num: int
    line_num: int
    word_num: int
    left: int
    top: int
    width: int
    height: int
    conf: float
    text: str


class ImageToDataResponse(BaseModel):
    image_data: list[OCRData]


class TranslateImageTextRequest(BaseModel):
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    image: str


class Error(BaseModel):
    error: str


# import importlib.util
# import inspect
# import sys
# import os
#
# from os import path as path_utils
# from types import ModuleType
#
#
# START_MODULE_PATH = {
#     'DEV': '..\\..\\api_server\\src',
#     'PROD': '..'
# }
#
# MODULE_NAMES = {
#     'API': {
#         'name': 'api.py',
#         'path': 'domain'},
#     'OCR': {
#         'name': 'ocr.py',
#         'path': 'domain'},
#     'LOGGING': {
#         'name': 'logging.py',
#         'path': 'service'}
# }
#
#
# def get_full_module_path(module_name: str, path_type: str) -> str:
#     return (START_MODULE_PATH[path_type]
#             + '\\' + MODULE_NAMES[module_name.upper()]['path'] + '\\'
#             + MODULE_NAMES[module_name.upper()]['name'])
#
#
# def get_module_path_type(module_name: str) -> str:
#     """
#     Функция проверки наличия пути модуля
#     :return: Тип пути модуля
#     """
#     # Перебор путей к модулям
#     for path_type, path in START_MODULE_PATH.items():
#         # Проверка наличия файла по пути к модулю
#         if path_utils.isfile(get_full_module_path(module_name, path_type)):
#             return path_type
#     raise RuntimeError('Модули домена не найдены')
#
#
# def get_module_from_file(module_name: str,
#                          module_link: str = '',
#                          sub_module_loc: list[str] = None
#                          ) -> ModuleType:
#     """
#     Функция получения объекта модуля из файла модуля
#     :param module_name: Имя модуля
#     :param module_link: Ссылочное имя модуля
#     :param sub_module_loc: Список путей поиска модулей
#     :return: Объект модуля
#     """
#     # Получение пути к файлу модуля
#     module_path_type = get_module_path_type(module_name)
#     module_path = get_full_module_path(module_name, module_path_type)
#     # Получение спецификации модуля и объекта модуля
#     spec = importlib.util.spec_from_file_location(
#         module_name if module_link == '' else module_link,
#         module_path,
#         submodule_search_locations=sub_module_loc)
#     module = importlib.util.module_from_spec(spec)
#     sys.modules[module_name if module_link == '' else module_link] = module
#     spec.loader.exec_module(module)
#     return module
#
#
# def get_class_from_module(class_name: str, module: ModuleType):
#     """
#     Функция получения класса из объекта модуля
#     :param class_name: Имя класса
#     :param module: Объект модуля
#     :return: Описание класса (не инстанция!!!)
#     """
#     # Перебор объектов модуля
#     for member in inspect.getmembers(module):
#         if not inspect.isclass(member[1]):
#             continue
#         # Если объект класс, то вернуть его описание
#         if member[0] == class_name:
#             return member[1]
#
#
# def get_func_from_module(func_name: str, module: ModuleType):
#     """
#     Функция получения функции из объекта модуля
#     :param func_name: Имя функции
#     :param module: Объект модуля
#     :return: Описание класса (не инстанция!!!)
#     """
#     # Перебор объектов модуля
#     for member in inspect.getmembers(module):
#         if not inspect.isfunction(member[1]):
#             continue
#         # Если объект функция, то вернуть его описание
#         if member[0] == func_name:
#             return member[1]
#

# logging_path = get_full_module_path(
#     'logging',
#     get_module_path_type('logging'))
# print(logging_path)
# if logging_path not in sys.path:
#     sys.path.append(logging_path)
#
# ocr_path = get_full_module_path(
#     'ocr',
#     get_module_path_type('ocr'))
# print(ocr_path)
# if ocr_path not in sys.path:
#     sys.path.append(ocr_path)


# for path_hook in sys.path_hooks:
#     print(path_hook)
#
# for meta_path1 in sys.meta_path:
#     print(meta_path1)

# for name, finder in list(sys.path_importer_cache.items()):
#     if name != 'C:\\Users\\CatBoss\\PycharmProjects\\neuro_screen_scanner\\desktop_client\\src\\ui':
#         continue
#     print(finder.path_hook())
#
# # Импорт модулей и классов из доменной модели сервиса
# server_logging_domain_py = get_module_from_file('logging',
#                                                 module_link='..service.logging')
# get_logger = get_func_from_module('get_logger', server_logging_domain_py)
#
# server_ocr_domain_py = get_module_from_file('ocr',
#                                             module_link='.ocr')
# OCRData = get_class_from_module('OCRData', server_ocr_domain_py)
#
# server_api_domain_py = get_module_from_file('api')
# Error = get_class_from_module('Error', server_api_domain_py)
# ImageToTextRequest = get_class_from_module('ImageToTextRequest', server_api_domain_py)
#
# print(type(OCRData))
# print(type(Error))
