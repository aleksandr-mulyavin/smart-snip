import base64
import os

from . import ocr


def test_recognize_text_from_image():
    """
    """
    with open(os.path.join('api_server',
                           'assets',
                           'test.png'), 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read())
        result = ocr.image_to_string(encoded_string)
        assert len(result) > 0
        assert 'from' in result
        assert 'fastapi' in result
        assert 'import' in result
        assert 'status' in result


def test_recognize_exception():
    """
    """
    result = ocr.image_to_string('')

    assert result == ''
