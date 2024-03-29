from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QColorDialog
from PyQt5.QtGui import QColor


class ColorSelectComboBoxWidget(QComboBox):
    selectedColor = QtCore.pyqtSignal(QColor)

    def __init__(self, parent=None, with_default=False, enableUserDefColors=True):
        super(ColorSelectComboBoxWidget, self).__init__(parent)

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._currentColor: QColor = None
        if with_default:
            self.add_сolor(QtGui.QColor(255, 0, 0, 255))
            self.add_сolor(QtGui.QColor(0, 255, 0, 255))
            self._currentColor = QColor(0, 255, 0, 255)
            self._color_selected(0)
            print(self.itemData(0))
            self._currentColor = self.itemData(0)

        self._userDefEntryText = 'Свой цвет'

        if enableUserDefColors:
            self.addItem(self._userDefEntryText)


        self.activated.connect(self._color_selected)

    def add_сolors(self, colors):
        for a_color in colors:
            if not (isinstance(a_color, QColor)):
                a_color = QColor(a_color)
            if self.findData(a_color) == -1:
                self.addItem('', userData=a_color)
                self.setItemData(self.count() - 1, QColor(a_color), Qt.BackgroundRole)

    def add_сolor(self, color):
        self.add_сolors([color])

    def set_сolor(self, color):
        self.add_сolor(color)
        self._color_selected(self.findData(color), False)

    def get_сurrent_сolor(self) -> QColor:
        return self._currentColor

    def _color_selected(self, index, emitSignal=True):
        if self.itemText(index) == '':
            self._currentColor = self.itemData(index)
            if emitSignal:
                self.selectedColor.emit(self._currentColor)
        elif self.itemText(index) == self._userDefEntryText:
            new_color = QColorDialog.getColor(self._currentColor if self._currentColor else Qt.white)
            if new_color.isValid():
                self.add_сolor(new_color)
                self._currentColor = new_color
                if emitSignal:
                    self.selectedColor.emit(self._currentColor)

        # make sure that current color is displayed
        if self._currentColor:
            self.setCurrentIndex(self.findData(self._currentColor))
            self.lineEdit().setStyleSheet("background-color: " + self._currentColor.name())