import base64
from django.shortcuts import render, HttpResponse
from .translate_text import iso_639_1_languages, get_to_text_translate
from .forms import UploadFileForm, TranslatorForm
from .api import APIImageHandler


def home(request):
    return render(request, 'main/home.html')


def app(request):
    source_text = 'Work'
    translated_text = get_to_text_translate(source_text, 'ru')
    translator_form = TranslatorForm(initial={
        'source_text': source_text,
        'translated_text': translated_text,
    })
    upload_file = UploadFileForm()
    encoded_image = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'upload_file':
            upload_file = UploadFileForm(request.POST, request.FILES)
            if upload_file.is_valid():
                image_data = request.FILES['file'].read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
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
        }
    )


def translate_image(request):
    img_src = request.POST.get("img_src")
    translated_image = ''
    if img_src is not None:
        image_handler = APIImageHandler(
            encoded_image=img_src.removeprefix('data:image/jpeg;base64,')
        )
        translated_image = image_handler.translate_image()
    return HttpResponse(content=translated_image)


def about(request):
    return render(request, 'main/about.html')
