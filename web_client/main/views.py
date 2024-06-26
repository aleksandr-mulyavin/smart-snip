import base64
from django.shortcuts import render, HttpResponse
from .translate_text import iso_639_1_languages, get_to_text_translate
from .forms import UploadFileForm, TranslatorForm
from .api import APIImageHandler


def home(request):
    """
    Функция home с помощью render объединяет main/home.html шаблон с предоставленным контекстом и возвращает объект
    HttpResponse с отрендеренным HTML-текстом.
    """
    return render(request, 'main/home.html')


def app(request):
    """
    Функция app с помощью render объединяет main/app.html шаблон с предоставленным контекстом и возвращает объект
    HttpResponse с отрендеренным HTML-текстом.
    """
    source_text = 'Work'
    translated_text = get_to_text_translate(source_text, 'ru')
    translator_form = TranslatorForm(initial={
        'source_text': source_text,
        'translated_text': translated_text,
    })

    # upload_file инициализирует форму для отображения в шаблоне
    upload_file = UploadFileForm()
    image_filename = ''
    encoded_image = None
    translated_image = None

    # Проверка метода POST. Если пользовать загрузил изображение и оно валидно, получаем файл в кодировке base64
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'upload_file':
            upload_file = UploadFileForm(request.POST, request.FILES)
            if upload_file.is_valid():
                image_filename = upload_file.cleaned_data['file'].name
                image_data = request.FILES['file'].read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                request.session['source_image'] = encoded_image
                request.session['image_filename'] = image_filename
                image_handler = APIImageHandler(
                    encoded_image=encoded_image
                )
                source_text = image_handler.image_to_text()
                translated_text = get_to_text_translate(source_text, 'ru')
                translator_form = TranslatorForm(initial={
                    'source_text': source_text,
                    'translated_text': translated_text,
                })

        elif form_type == 'translator_form':
            translator_form = TranslatorForm(request.POST)
            if translator_form.is_valid():
                source_text = translator_form.cleaned_data['source_text']
                output = translator_form.cleaned_data['lang_elements']
                # функция с переводом
                translated_text = get_to_text_translate(source_text, output)
                translator_form = TranslatorForm(initial={
                    'source_text': source_text,
                    'translated_text': translated_text,
                })
            encoded_image = request.session.get('source_image')
            image_filename = request.session.get('image_filename')
            translated_image = request.session.get('translated_image')
    else:
        if request.session.get('source_image') is not None:
            request.session.clear()

    display_download_button = 'none' if translated_image is None else 'block'

    return render(
        request,
        'main/app.html',
        {
            "translator_form": translator_form,
            "iso_639_1_languages": iso_639_1_languages,
            "upload_file": upload_file,
            "show_translate_image_button": encoded_image is not None,
            "encoded_image": encoded_image,
            "show_encoded_image": encoded_image is not None,
            'image_filename': image_filename,
            'translated_image': translated_image,
            "display_download_image_button": display_download_button,
        }
    )


def translate_image(request):
    img_src = request.POST.get("img_src")
    selected_lang = request.POST.get("lang")
    if selected_lang is None:
        selected_lang = 'ru'
    translated_image = ''
    if img_src is not None:
        image_handler = APIImageHandler(
            encoded_image=img_src.removeprefix('data:image;base64,')
        )
        translated_image = image_handler.translate_image(selected_lang)
        request.session['translated_image'] = translated_image
    return HttpResponse(content=translated_image)


def about(request):
    """
    Функция about с помощью render объединяет main/about.html шаблон с предоставленным контекстом и возвращает объект
    HttpResponse с отрендеренным HTML-текстом.
    """
    return render(request, 'main/about.html')
