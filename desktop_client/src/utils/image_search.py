import io
import json
import requests
import webbrowser

from PIL.Image import Image


def get_link_for_search_in_yandex(image: Image) -> str:
    search_url = 'https://yandex.ru/images/search'

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')

    files = {'upfile': ('blob', img_byte_arr.getvalue(), 'image/jpeg')}
    params = {'rpt': 'imageview',
              'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    return search_url + '?' + query_string


def open_search_in_browser(image: Image) -> None:
    search_url = get_link_for_search_in_yandex(image)
    if not search_url:
        return
    webbrowser.open(search_url)
