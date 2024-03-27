# Импортируем библиотеки
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from googletrans import Translator

class modal_translate(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    #Функция для копирования текста
    def copy_text(self):
        text = self.output_text.toPlainText()
        QApplication.clipboard().setText(text)

    #Функция для вставки текста
    def paste_text(self):
        text = QApplication.clipboard().text()
        self.entry_text.insertPlainText(text)

    # Функция для обработки нажатия кнопки "перевести"
    def translate_text(self):
        translator = Translator()
        translated_text = translator.translate(self.entry_text.toPlainText(), dest=self.selected_language.currentText()).text
        self.output_text.setPlainText(translated_text)

    # Создание основного окна
    def initUI(self):
        self.setWindowTitle("Выберите язык и введите/вставьте текст, который нужно перевести: ")

        # вертикальное расположение элементов интерфейса
        layout = QVBoxLayout()

        # Поле для ввода текста
        self.entry_text = QTextEdit()
        self.entry_text.setFixedHeight(200) # длинна поля
        self.entry_text.setFixedWidth(600)  # ширина поля
        layout.addWidget(self.entry_text)

        # Кнопка вставки текста
        self.btn_paste = QPushButton("Вставить текст для перевода")
        self.btn_paste.clicked.connect(self.paste_text)
        layout.addWidget(self.btn_paste)

        # Выпадающий список с выбором языка
        languages = ["English", "French", "German", "Russian"] # Список доступных языков
        self.selected_language = QComboBox()
        self.selected_language.addItems(languages)
        self.selected_language.setCurrentText("English") # Устанавливаем язык по умолчанию - английский
        layout.addWidget(self.selected_language, alignment=Qt.AlignCenter)  # выравнивание по центру

        # Кнопка перевести
        self.translate_button = QPushButton("Перевести")
        self.translate_button.clicked.connect(self.translate_text)
        layout.addWidget(self.translate_button)

        # Поле для вывода переведенного текста
        self.output_text = QTextEdit()
        self.output_text.setFixedHeight(200) # длина поля
        self.output_text.setFixedWidth(600)  # ширина поля
        layout.addWidget(self.output_text)

        # Кнопка для копирования
        self.btn_copy = QPushButton("Копировать перевод")
        self.btn_copy.clicked.connect(self.copy_text)
        layout.addWidget(self.btn_copy)

        self.setLayout(layout)
        self.show()