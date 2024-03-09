import base64
import os

from src.service.ocr import image_to_string


def test_recognize_text_from_image(mocker):
    """
    """
    mocker.patch(
        'pytesseract.image_to_string',
        return_value='some text'
    )

    with open(os.path.join('api_server',
                           'test',
                           'assets',
                           'test.png'), 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read())

        result = image_to_string(encoded_string)

        assert len(result) > 0


def test_recognize_exception():
    """
    """
    result = image_to_string('')

    assert result == ''
