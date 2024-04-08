"""
Модуль с виджетом для выбора цвета через выпадающий список
"""
import logging

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QColorDialog, QWidget
from PyQt5.QtGui import QColor


LOGGER = logging.getLogger(__name__)


class ColorSelectComboBoxWidget(QComboBox):
    """
    Виджет для выбора цвета через выпадающий список
    """

    onColorSelectedEvent = QtCore.pyqtSignal(QColor)
    """Событие выбора цвета пользователем"""

    def __init__(self,
                 parent: QWidget = None,
                 withDefault: bool = False,
                 enableUserDefColors: bool = False):
        """
        Конструктор объекта
        :param parent: Родительский виджет
        :param withDefault: Заполнить цветами по умолчанию
        :param enableUserDefColors: Позволить пользователю указать цвет
        """
        super(ColorSelectComboBoxWidget, self).__init__(parent)

        # Установим объект изменяемым,
        # но запретим редактирование надписей
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        self._current_color: QColor = QColor()
        """Текущий цвет"""

        self._userDefEntryText = 'Свой цвет'
        """Текст пункта для выбора своего цвета"""

        if withDefault:
            # Добавление цветов по умолчанию
            self.add_color(QtGui.QColor(255, 0, 0, 255))
            self.add_color(QtGui.QColor(0, 255, 0, 255))
            self._select_color(0)
            self._current_color = self.itemData(0)

        if enableUserDefColors:
            # Добавление пункта выбора цвета пользователем
            self.addItem(self._userDefEntryText)

        # Подключение события выбора виджета к методу выбора цвета
        self.activated.connect(self._select_color)

    def add_colors(self, colors: list[QColor]) -> None:
        """
        Добавление цветов в набор
        :param colors: Список цветов
        """
        for color in colors:
            # Приведение объекта к типу цвета
            if not (isinstance(color, QColor)):
                color = QColor(color)
            # Если цвет ранее не добавлялся, то добавим
            if self.findData(color) == -1:
                self.addItem('', userData=color)
                self.setItemData(self.count() - 1,
                                 QColor(color),
                                 Qt.BackgroundRole)

    def add_color(self, color: QColor) -> None:
        """
        Добавление цвета в набор
        :param color: Цвет
        """
        self.add_colors([color])

    def set_color(self, color: QColor) -> None:
        """
        Выбор текущего цвета
        :param color: Цвет
        """
        # Добавление цвета (вдруг нету)
        self.add_color(color)
        self._select_color(self.findData(color), False)

    def get_current_color(self) -> QColor:
        return self._current_color

    def _select_color(self, index: int, emitSignal: bool = True) -> None:
        """
        Обработка выбора цвета
        :param index: Индекс выбираемого цвета
        :param emitSignal: Запуск события
        """
        if self.itemText(index) == '':
            # Если выбран цвет, то установим его
            # и вызовем событие завершения выбора
            self._current_color = self.itemData(index)
            if emitSignal:
                self.onColorSelectedEvent.emit(self._current_color)
        elif self.itemText(index) == self._userDefEntryText:
            # Если выбран пункт пользовательского выбора цвета,
            # то покажем окно выбора цвета и вызовем событие
            new_color = QColorDialog.getColor(
                self._current_color if self._current_color else Qt.white)
            if new_color.isValid():
                self.add_color(new_color)
                self._current_color = new_color
                if emitSignal:
                    self.onColorSelectedEvent.emit(self._current_color)

        # Сделаем активным выбранный цвет, если он есть
        if self._current_color:
            self.setCurrentIndex(self.findData(self._current_color))
            self.lineEdit().setStyleSheet(
                "background-color: " + self._current_color.name())
