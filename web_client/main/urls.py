from django.urls import path
from . import views

# Определение набора URL-шаблонов для Django-приложения, который используется для маршрутизации запросов к
# соответствующим представлениям (views)
urlpatterns = [
    path('', views.home, name='home'),
    path('app', views.app, name='app'),
    path('about', views.about, name='about'),
    path('translate_image', views.translate_image, name='translate_image')
]
