from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app', views.app, name='app'),
    path('about', views.about, name='about')
]
