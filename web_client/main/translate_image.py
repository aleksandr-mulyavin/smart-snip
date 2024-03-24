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


class TranslateImageHandler():
    def __init__(self, request):
        self.request = request

    def process_request(self):
        if self.request.method == 'POST':
            form = ImageUploadForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                image_data = self.request.FILES['image'].read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')

                api_url = os.getenv('API_URL')
                api_method = os.getenv('API_TRANSLATE_IMAGE')
                token = os.getenv('API_TOKEN')

                translate_request = TranslateImageTextRequest(
                    image=encoded_image,
                    to_lang=''
                )
                headers = {'X-API-key': '-' if token is None else token}
                response = requests.post(
                    url=f'{api_url}/{api_method}',
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
