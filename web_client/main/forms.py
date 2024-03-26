from django import forms
from .translate_text import iso_639_1_languages


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="")


class TranslatorForm(forms.Form):
    """
    Создает форму для выбора из выпадающего списка названия языков
    """
    source_text = forms.CharField(widget=forms.Textarea)
    lang_elements = forms.ChoiceField(choices=iso_639_1_languages, label='')
    translated_text = forms.CharField(widget=forms.Textarea)
