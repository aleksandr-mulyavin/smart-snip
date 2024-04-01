from django import forms
from .translate_text import iso_639_1_languages


class UploadFileForm(forms.Form):
    """
    Создает форму с одним полем для загрузки изображения
    """
    file = forms.ImageField(label="")


class TranslatorForm(forms.Form):
    """
    Создает формы:
    - поле для вывода исходного текста
    - выпадающий список для выбора языка, на который нужно перевести текст
    - поле для вывода теста после его перевода на другой язык
    """
    source_text = forms.CharField(
        widget=forms.Textarea,
        label='Исходный текст'
    )
    lang_elements = forms.ChoiceField(
        choices=iso_639_1_languages,
        label=''
    )
    translated_text = forms.CharField(
        widget=forms.Textarea,
        label='Перевод',
        required=False,
    )
