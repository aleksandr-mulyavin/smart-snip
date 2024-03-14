from django.shortcuts import render
from .translate_text import tran, t


def index(request):
    return render(request, 'main/app.html')


def about(request):
    s = t()
    c = tran(s)
    return render(request, 'main/about.html', {"tran": c, "t": s})
