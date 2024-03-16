import os
from PIL import Image
from api_server.src.service.image import ImageHandler


def test_erase_and_draw_text():

    image = Image.open(os.path.join('api_server',
                                    'test',
                                    'assets',
                                    'test.png'))
    image_handler = ImageHandler(image)

    result = 'level	page_num	block_num	par_num	line_num'
    '   word_num	left	top	width	height	conf	text\n'

    data = [[row for row in line.split('\t')] for line in result.split('\n')]

    image_handler.erase_text(data[1:])
    image_handler.draw_text(data[1:])

    assert True
