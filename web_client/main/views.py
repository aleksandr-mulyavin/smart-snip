from django.shortcuts import render
from .translate_text import t
from .screenshot import result_screenshot


def home(request):
    return render(request, 'main/home.html')


def app(request):
    s = t()
    # c = tran(s)
    # screenshot = result_screenshot()
    return render(request, 'main/app.html', {"t": s})


def about(request):
    return render(request, 'main/about.html')
