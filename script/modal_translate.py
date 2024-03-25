# Импортируем библиотеки
import tkinter as tk
from tkinter import ttk
from googletrans import Translator

#Функция для копирования текста
def copy_text():
    text = output_text.get('1.0', 'end-1c')
    root.clipboard_clear()
    root.clipboard_append(text)

#Функция для вставки текста
def paste_text():
    text = root.clipboard_get()
    entry_text.insert(tk.END, text)

# Функция для обработки нажатия кнопки
def translate_text():
    translator = Translator()
    translated_text = translator.translate(entry_text.get("1.0", "end"), dest=selected_language.get()).text
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, translated_text)

# Создание основного окна
root = tk.Tk()
root.title("Выберите язык и введите/вставьте текст, который нужно перевести: ")

# Поле для ввода текста
entry_text = tk.Text(root, width=70,  height=10)
entry_text.pack(pady=10)

# Кнопка вставки текста
btn_paste = tk.Button(root, text="Вставить текст для перевода", command=paste_text)
btn_paste.pack()

# Выпадающий список с выбором языка
languages = ["English", "French", "German", "Russian"]  # Список доступных языков
selected_language = ttk.Combobox(root, values=languages)
selected_language.pack(pady=5)
selected_language.set("English")  # Устанавливаем язык по умолчанию - английский

# Кнопка для запуска перевода
translate_button = tk.Button(root, text="Перевести", command=translate_text)
translate_button.pack(pady=5)

# Поле для вывода переведенного текста
output_text = tk.Text(root, height=10, width=70)
output_text.pack(pady=10)

# Кнопка для копирования
btn_copy = tk.Button(root, text="Копировать перевод", command=copy_text)
btn_copy.pack()

root.mainloop()