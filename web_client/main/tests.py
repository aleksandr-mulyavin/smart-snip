from django.core.files.uploadedfile import SimpleUploadedFile
from web_client.main.forms import UploadFileForm
from web_client.main.views import handle_uploaded_file
from django.test import RequestFactory
from django.urls import reverse
from web_client.main.views import home, app, about
import pytest


def test_handle_uploaded_file():
    # Создаем объект SimpleUploadedFile, имитирующий загруженный файл
    file = SimpleUploadedFile(
        name="logo.png",
        content=b"binary content"
    )

    # Вызываем функцию с созданным объектом SimpleUploadedFile
    result = handle_uploaded_file(file)
    # Проверяем, что функция вернула ожидаемый путь к файлу
    assert result == "main/image/logo.png"



# def test_upload_file_form():
#
#     uploaded_file = SimpleUploadedFile(name="logo.png", content=b"binary content")
#     form = UploadFileForm(files={'file': uploaded_file})
#
#     assert form.is_valid()


# def test_home_view():
#     factory = RequestFactory()
#     request = factory.get(reverse('home'))
#     response = home(request)
#     assert response.status_code == 200
#     assert response.template_name == 'main/home.html'
#
#
# def test_app_view():
#     factory = RequestFactory()
#     request = factory.get(reverse('app'))
#     response = app(request)
#     assert response.status_code == 200
#     assert response.template_name == 'main/app.html'

# def test_app_view():
#     factory = RequestFactory()
#     request = factory.get(reverse('about'))
#     response = about(request)
#     assert response.status_code == 200
#     assert response.template_name == 'main/about.html'

