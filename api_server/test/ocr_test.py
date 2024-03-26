import base64
import os

from api_server.src.service.ocr import (
    image_to_string,
    image_to_data
)


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


def test_getting_ocr_data_from_image(mocker):
    """
    """
    mocker.patch(
        'pytesseract.image_to_data',
        return_value='level	page_num	block_num	par_num	line_num'
        '	word_num	left	top	width	height	conf	text\n'
        '5	1	1	1	1	1	517	18	170	29	96.582634	Offensive\n'
    )

    with open(os.path.join('api_server',
                           'test',
                           'assets',
                           'test.png'), 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read())

        result = image_to_data(encoded_string)

        assert type(result) is list
        assert len(result) > 0


def test_recognize_exception():
    """
    """
    result = image_to_string('')

    assert result == ''
