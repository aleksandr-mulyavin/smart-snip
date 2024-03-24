from django.shortcuts import render
from .translate_text import t, iso_639_1_languages, get_to_text_translate
from .forms import UploadFileForm, DictLanguage


def home(request):
    return render(request, 'main/home.html')


def handle_uploaded_file(f):
    """
    Позволяет сохранить файл, который загрузил пользователь
    """
    file_path = f"main/static/main/image/{f.name}"
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if file_path:
        return file_path[12:]  # Получаем путь к static, куда сохранился файл для отображения на веб-сайте
    else:
        return None


def app(request):
    s = t()  # временная функция с текстом
    result_translate = get_to_text_translate(s, 'ru')  # функция с переводом
    language_and_code = DictLanguage()  # форма с ниспадающим списком
    upload_file = UploadFileForm()
    file_path_static = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'upload_file':
            upload_file = UploadFileForm(request.POST, request.FILES)
            if upload_file.is_valid():
                file_path_static = handle_uploaded_file(upload_file.cleaned_data['file'])  # получение загруженного файла пользователем

        elif form_type == 'change_language':
            lang_elements = request.POST.get("lang_elements")
            output = lang_elements
            result_translate = get_to_text_translate(s, output)  # функция с переводом

    return render(request, 'main/app.html', {"language_and_code": language_and_code,
                                             "result_translate": result_translate,
                                             "t": s,
                                             "iso_639_1_languages": iso_639_1_languages,
                                             "upload_file": upload_file,
                                             "file_path_static": file_path_static})


def about(request):
    return render(request, 'main/about.html')
