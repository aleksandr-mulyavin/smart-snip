import requests
import base64

from io import BytesIO
from PIL.Image import Image

from ..api_models import Error, ImageToTextRequest
from ..api_models import ImageToDataResponse

API_METHOD = 'image_to_text'


def call_image_to_text(url: str, token: str, image: Image) -> str:
    print(url, token)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    headers = {'X-API-key': token,
               'Content-Type': 'application/json'}

    request = ImageToTextRequest(
        image=img_str)

    try:
        http_response = requests.post(f'{url}{API_METHOD}', headers=headers, json=request.model_dump(mode='json'))
        print(http_response, http_response.text)
        if http_response.status_code == requests.codes.ok:
            return http_response.text
    except Exception as e:
        print(e)


def call_image_to_data(url: str, token: str, image: Image) -> ImageToDataResponse:
    print(url, token)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    headers = {'X-API-key': token,
               'Content-Type': 'application/json'}

    request = ImageToTextRequest(
        image=img_str)

    try:
        http_response = requests.post(f'{url}{API_METHOD}', headers=headers, json=request.model_dump(mode='json'))
        print(http_response, http_response.text)
        if http_response.status_code == requests.codes.ok:
            return ImageToDataResponse(**http_response.json())
    except Exception as e:
        print(e)
