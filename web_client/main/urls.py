from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app', views.app, name='app'),
    path(
        'translate_image',
        views.translate_image,
        name='translate_image'
    ),
    path('about', views.about, name='about')
]
