import importlib.util
import inspect
import sys

from pathlib import Path
from types import ModuleType


def find_module_file_path(module_name: str,
                          from_path: Path = None) -> Path | None:
    _from_path = from_path if from_path is not None else \
                 Path(__file__).parent.resolve()

    for path in _from_path.rglob(module_name):
        if not path.is_file():
            continue
        return path

    if _from_path.parents and not from_path:
        max_iteration: int = 4
        if max_iteration > len(_from_path.parents):
            max_iteration = len(_from_path.parents)
        for i in range(max_iteration):
            inside_path = find_module_file_path(
                module_name,
                _from_path.parents[i])
            if inside_path:
                return inside_path
    return None


def get_full_module_path(module_name: str) -> str:
    module_path = find_module_file_path(module_name)
    if module_path is None:
        return ''
    print(str(module_path))
    return str(module_path)


def get_module_from_file(module_name: str,
                         module_link: str = '',
                         sub_module_loc: list[str] = None
                         ) -> ModuleType:
    """
    Функция получения объекта модуля из файла модуля
    :param module_name: Имя модуля
    :param module_link: Ссылочное имя модуля
    :param sub_module_loc: Список путей поиска модулей
    :return: Объект модуля
    """
    # Получение пути к файлу модуля
    module_path = get_full_module_path(module_name)
    # Получение спецификации модуля и объекта модуля
    spec = importlib.util.spec_from_file_location(
        module_name if module_link == '' else module_link,
        module_path,
        submodule_search_locations=sub_module_loc)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name if module_link == '' else module_link] = module
    spec.loader.exec_module(module)
    return module


def get_class_from_module(class_name: str, module: ModuleType):
    """
    Функция получения класса из объекта модуля
    :param class_name: Имя класса
    :param module: Объект модуля
    :return: Описание класса (не инстанция!!!)
    """
    # Перебор объектов модуля
    for member in inspect.getmembers(module):
        if not inspect.isclass(member[1]):
            continue
        # Если объект класс, то вернуть его описание
        if member[0] == class_name:
            return member[1]


def get_func_from_module(func_name: str, module: ModuleType):
    """
    Функция получения функции из объекта модуля
    :param func_name: Имя функции
    :param module: Объект модуля
    :return: Описание класса (не инстанция!!!)
    """
    # Перебор объектов модуля
    for member in inspect.getmembers(module):
        if not inspect.isfunction(member[1]):
            continue
        # Если объект функция, то вернуть его описание
        if member[0] == func_name:
            return member[1]
