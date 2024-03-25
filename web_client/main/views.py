from django.shortcuts import render
from .translate_text import t, iso_639_1_languages, get_to_text_translate, DictLanguage
from .translate_image import APIImageHandler


def home(request):
    return render(request, 'main/home.html')


def app(request):
    s = t() # временная функция с текстом
    result_translate = get_to_text_translate(s, 'ru') # функция с переводом
    if request.method == "POST":
        user_id = request.POST.get("lang_elements")
        output = user_id
        result_translate = get_to_text_translate(s, output) # функция с переводом
        language_and_code = DictLanguage()
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


def translate_image(request):
    return APIImageHandler(
        request=request
    ).process_request()


def about(request):
    return render(request, 'main/about.html')
