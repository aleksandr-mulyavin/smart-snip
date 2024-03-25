import os
import base64
import requests
from .models import (
    APIConfig,
    ImageToTextRequest,
    TranslateImageTextRequest,
    TranslateImageTextResponse
)


class APIImageHandler():
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.api_config = self.__get_config()

    def image_to_text(self) -> str:
        encoded_image = self.__encode_image()
        if encoded_image is None:
            return ''

        response = self.__send_request(
            self.api_config.image_to_text,
            ImageToTextRequest(
                image=encoded_image,
                lang=''
            )
        )

        return response.text

    def translate_image(self) -> str:
        encoded_image = self.__encode_image()
        if encoded_image is None:
            return ''

        response = self.__send_request(
            self.api_config.translate_image,
            TranslateImageTextRequest(
                image=encoded_image,
                to_lang=''
            )
        )
        translated = TranslateImageTextResponse.model_validate(
            response.json()
        )

        return translated.image

    def __send_request(self, method, request) -> requests.Response:
        headers = {'X-API-key': self.api_config.token}
        response = requests.post(
            url=f'{self.api_config.url}/{method}',
            headers=headers,
            json=request.model_dump(),
        )
        return response

    def __encode_image(self) -> str:
        encoded_image = ''
        with open(self.image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
        return encoded_image

    @staticmethod
    def __get_config() -> APIConfig:
        url = os.getenv('API_URL')

        image_to_text_method = os.getenv('API_IMAGE_TO_TEXT')
        if image_to_text_method is None:
            image_to_text_method = 'image_to_text'

        translate_image_method = os.getenv('API_TRANSLATE_IMAGE')
        if translate_image_method is None:
            translate_image_method = 'translate_image_text'

        token = os.getenv('API_TOKEN')
        if token is None:
            token = '-'

        return APIConfig(
            url=url,
            token=token,
            image_to_text=image_to_text_method,
            translate_image=translate_image_method,
        )
