import os
from django.shortcuts import render
from .translate_text import t, iso_639_1_languages, get_to_text_translate
from .forms import UploadFileForm, DictLanguage
from .api import APIImageHandler

UPLOADED_DIR = 'main/static/main/image/uploaded'


def home(request):
    return render(request, 'main/home.html')


def handle_uploaded_file(f):
    """
    Позволяет сохранить файл, который загрузил пользователь
    """
    if not os.path.exists(UPLOADED_DIR):
        os.makedirs(UPLOADED_DIR)
    file_path = f"{UPLOADED_DIR}/{f.name}"
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if file_path:
        # Получаем путь к файлу и путь к static,
        # куда сохранился файл для отображения на веб-сайте
        return file_path, file_path[12:]
    else:
        return None, None


def app(request):
    s = t()  # временная функция с текстом
    result_translate = get_to_text_translate(s, 'ru')  # функция с переводом
    language_and_code = DictLanguage()  # форма с ниспадающим списком
    upload_file = UploadFileForm()
    file_path = None
    file_path_static = None
    translated_image = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'upload_file':
            upload_file = UploadFileForm(request.POST, request.FILES)
            if upload_file.is_valid():
                # получение загруженного файла пользователем
                file_path, file_path_static = handle_uploaded_file(
                    upload_file.cleaned_data['file']
                )
                if file_path is not None:
                    image_handler = APIImageHandler(image_path=file_path)
                    s = image_handler.image_to_text()
                    result_translate = get_to_text_translate(s, 'ru')

        elif form_type == 'translate_image':
            file_path = request.POST.get("file_path")
            if file_path is not None:
                image_handler = APIImageHandler(image_path=file_path)
                translated_image = image_handler.translate_image()

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
            "file_path": file_path,
            "file_path_static": file_path_static,
            "translated_image": translated_image,
        }
    )


def about(request):
    return render(request, 'main/about.html')
