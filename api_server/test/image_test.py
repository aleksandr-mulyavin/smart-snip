import os
from PIL import Image
from api_server.src.domain.api import OCRData
from api_server.src.service.image import ImageHandler
from api_server.src.service.translating import Translator


def test_translate_text():

    image = Image.open(os.path.join('api_server',
                                    'test',
                                    'assets',
                                    'test.png'))
    image_handler = ImageHandler(
        image=image,
        translator=Translator(from_lang='eng', to_lang='rus')
    )

    result = 'level	page_num	block_num	par_num	line_num'
    '   word_num	left	top	width	height	conf	text\n'

    data = [line for line in result.split('\n')]
    image_data = [OCRData.from_str(line) for line in data[1:]]

    image_handler.translate_text(image_data)

    assert True


def test_determine_backround_color():

    image = Image.open(os.path.join('api_server',
                                    'test',
                                    'assets',
                                    'test.png'))
    image_handler = ImageHandler(
        image=image,
        translator=Translator(from_lang='eng', to_lang='rus')
    )

    result = image_handler.determine_colors(
        (0, 0, 50, 40)
    )

    assert len(result) == 2
    assert len(result[0]) == 4
    assert len(result[1]) == 4
