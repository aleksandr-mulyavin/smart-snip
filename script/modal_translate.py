# Импортируем библиотеки
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from googletrans import Translator

#Функция для копирования текста
def copy_text():
    text = output_text.toPlainText()
    app.clipboard().setText(text)

#Функция для вставки текста
def paste_text():
    text = app.clipboard().text()
    entry_text.insertPlainText(text)

# Функция для обработки нажатия кнопки "перевести"
def translate_text():
    translator = Translator()
    translated_text = translator.translate(entry_text.toPlainText(), dest=selected_language.currentText()).text
    output_text.setPlainText(translated_text)

# Создание основного окна
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Выберите язык и введите/вставьте текст, который нужно перевести: ")

#вертикальное расположение элементов интерфейса
layout = QVBoxLayout()

# Поле для ввода текста
entry_text = QTextEdit()
entry_text.setFixedHeight(200) # длинна поля
entry_text.setFixedWidth(600)  # ширина поля
layout.addWidget(entry_text)

# Кнопка вставки текста
btn_paste = QPushButton("Вставить текст для перевода")
btn_paste.clicked.connect(paste_text)
layout.addWidget(btn_paste)

# Выпадающий список с выбором языка
languages = ["English", "French", "German", "Russian"] # Список доступных языков
selected_language = QComboBox()
selected_language.addItems(languages)
selected_language.setCurrentText("English") # Устанавливаем язык по умолчанию - английский
layout.addWidget(selected_language, alignment=Qt.AlignCenter)  # выравнивание по центру

# Кнопка перевести
translate_button = QPushButton("Перевести")
translate_button.clicked.connect(translate_text)
layout.addWidget(translate_button)

# Поле для вывода переведенного текста
output_text = QTextEdit()
output_text.setFixedHeight(200) # длина поля
output_text.setFixedWidth(600)  # ширина поля
layout.addWidget(output_text)

# Кнопка для копирования
btn_copy = QPushButton("Копировать перевод")
btn_copy.clicked.connect(copy_text)
layout.addWidget(btn_copy)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
