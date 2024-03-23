from django.shortcuts import render
from .translate_text import t, iso_639_1_languages, get_to_text_translate, DictLanguage


def home(request):
    return render(request, 'main/home.html')


def handle_uploaded_file(f):
    """
    Позволяет сохранить файл, который загрузил пользователь
    """
    with open(f"main/temp_files/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def app(request):
    s = t()  # временная функция с текстом
    result_translate = get_to_text_translate(s, 'ru')  # функция с переводом
    if request.method == "POST":
        lang_elements = request.POST.get("lang_elements")
        output = lang_elements
        result_translate = get_to_text_translate(s, output)  # функция с переводом
        language_and_code = DictLanguage()  # форма с ниспадающим списком
        handle_uploaded_file(request.FILES["file_upload"])  # получение загруженного файла пользователем
        return render(request, 'main/app.html', {"language_and_code": language_and_code,
                                                 "result_translate": result_translate,
                                                 "t": s,
                                                 "iso_639_1_languages": iso_639_1_languages})

    else:
        language_and_code = DictLanguage()
    return render(request, 'main/app.html', {"language_and_code": language_and_code,
                                             "result_translate": result_translate,
                                             "t": s,
                                             "iso_639_1_languages": iso_639_1_languages})


def about(request):
    return render(request, 'main/about.html')
