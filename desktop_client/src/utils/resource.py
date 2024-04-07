from pathlib import Path


class ResourceFinder(object):
    # Интсанция класса для шаблона - Одиночка
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Метод создания инстанции класса или возврата существующей
        инстанции (часть шаблона - Одиночка)
        """
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(ResourceFinder, cls).__new__(cls)
        elif cls.__init__.__name__ == '__init__':
            cls.__init__ = lambda *args, **kwargs: None
        return cls.__instance

    def __init__(self):
        """
        Конструктор класса
        """
        self._root_path = self.get_running_root()
        self._file_path_buffer: dict[str, Path] = {}

    @classmethod
    def get_running_root(cls) -> Path:
        """
        Получение пути запуска программы
        :return: Путь из которого запущена программа
        """
        return Path(__file__).parent.resolve()

    def find_resource_file(
            self, file_name: str, from_path: Path = None) -> Path | None:
        if from_path is not None:
            print(f'From path: {from_path}')

        _from_path = from_path if from_path is not None else self._root_path

        if file_name in self._file_path_buffer:
            return self._file_path_buffer[file_name]

        for path in _from_path.rglob(file_name):
            if not path.is_file():
                continue
            print(f'Path to {file_name}: {path.absolute()}')
            self._file_path_buffer[file_name] = path
            return path

        if _from_path.parents and not from_path:
            max_iteration: int = 3
            if max_iteration > len(_from_path.parents):
                max_iteration = len(_from_path.parents)
            for i in range(max_iteration):
                inside_path = self.find_resource_file(
                    file_name,
                    _from_path.parents[i])
                if inside_path:
                    return inside_path
        return None
