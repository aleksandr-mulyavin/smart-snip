import base64
from django.shortcuts import render, HttpResponse
from .translate_text import t, iso_639_1_languages, get_to_text_translate
from .forms import UploadFileForm, DictLanguage
from .api import APIImageHandler


def home(request):
    return render(request, 'main/home.html')


def app(request):
    s = t()  # временная функция с текстом
    result_translate = get_to_text_translate(s, 'ru')  # функция с переводом
    language_and_code = DictLanguage()  # форма с ниспадающим списком
    upload_file = UploadFileForm()
    encoded_image = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'upload_file':
            upload_file = UploadFileForm(request.POST, request.FILES)
            if upload_file.is_valid():
                image_data = request.FILES['file'].read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')

        elif form_type == 'change_language':
            lang_elements = request.POST.get("lang_elements")
            output = lang_elements
            # функция с переводом
            result_translate = get_to_text_translate(s, output)

    return render(
        request,
        'main/app.html',
        {
            "language_and_code": language_and_code,
            "result_translate": result_translate,
            "t": s,
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
