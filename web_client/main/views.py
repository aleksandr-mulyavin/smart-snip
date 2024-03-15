from django.shortcuts import render
from .translate_text import tran, t
from .screenshot import result_screenshot


def home(request):
    return render(request, 'main/home.html')


def app(request):
    s = t()
    c = tran(s)
    screenshot = result_screenshot()
    return render(request, 'main/app.html', {"tran": c, "t": s, "screenshot": screenshot})


def about(request):
    return render(request, 'main/about.html')
