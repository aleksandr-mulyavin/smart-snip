import os
import base64
import requests
from django import forms
from django.shortcuts import render
from .models import (
    TranslateImageTextRequest,
    TranslateImageTextResponse
)


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label='Выберите файл с изображением'
    )


class APIImageHandler():
    def __init__(self, request):
        self.request = request

    def translate_image(self):
        if self.request.method == 'POST':
            form = ImageUploadForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                image_data = self.request.FILES['image'].read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')

                api_config = self.__get_config()

                translate_request = TranslateImageTextRequest(
                    image=encoded_image,
                    to_lang=''
                )
                headers = {'X-API-key': api_config.token}
                response = requests.post(
                    url=f'{api_config.url}/{api_config.translate_image}',
                    headers=headers,
                    json=translate_request.model_dump(),
                )
                translated = TranslateImageTextResponse.model_validate(
                    response.json()
                )

                return render(
                    request=self.request,
                    template_name='main/translate_image.html',
                    context={
                        'form': form,
                        'encoded_image': translated.image,
                        'hidden_image': '',
                    }
                )
        else:
            form = ImageUploadForm()

        return render(
            request=self.request,
            template_name='main/translate_image.html',
            context={
                'form': form,
                'hidden_image': 'hidden',
            }
        )

    @staticmethod
    def __get_config():
        url = os.getenv('API_URL')
        translate_image_method = os.getenv('API_TRANSLATE_IMAGE')
        token = os.getenv('API_TOKEN')

        return {
            'url': url,
            'token': '-' if token is None else token,
            'translate_image': translate_image_method,
        }
