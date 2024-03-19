from django.shortcuts import render
from .translate_text import t, iso_639_1_languages, result, NewUserForm


def home(request):
    return render(request, 'main/home.html')


def app(request):
    s = t() # временная функция с текстом
    a = result(s, 'ru') # функция с переводом
    if request.method == "POST":
        user_id = request.POST.get("num")
        output = user_id
        a = result(s, output) # функция с переводом
        newuserform = NewUserForm()
        return render(request, 'main/app.html', {"form": newuserform, "a": a, "t": s, "iso_639_1_languages": iso_639_1_languages})

    else:
        newuserform = NewUserForm()
    return render(request, 'main/app.html', {"form": newuserform, "a": a, "t": s, "iso_639_1_languages": iso_639_1_languages})


def about(request):
    return render(request, 'main/about.html')
