# import os
import numpy as np
from sklearn.cluster import KMeans
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont
)

from .logging import get_logger
from ..domain.ocr import OCRData

logger = get_logger(__name__)


class ImageHandler():
    """Class for image processing: erase text, draw text.
    """
    def __init__(self, image: Image, translator):
        self.image = image
        self.translator = translator

    def _determine_colors(self, coords: tuple | None) -> tuple:
        """Determines the background color of the image using KMeans.
        """
        # prepare image for KMeans
        if coords is None:
            bands = self.image.split()
        else:
            bands = self.image.crop(coords).split()

        rgb = [np.asarray(band).flatten() for band in bands[:4]]
        reshape = np.array(
            [[rgb[0][i], rgb[1][i], rgb[2][i]] for i in range(rgb[0].shape[0])]
        )
        cluster = KMeans(n_clusters=3).fit(reshape)

        # get clusters to determine the primary colors
        centroids = cluster.cluster_centers_
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins=labels)
        hist = hist.astype('float')
        hist /= hist.sum()

        colors = sorted(
            [(percent, color) for (percent, color) in zip(hist, centroids)],
            reverse=True
        )

        if len(colors) > 1:
            background_color = colors[0][1]
            text_color = colors[1][1]
        elif len(colors) == 1:
            background_color = colors[0][1]
            text_color = (0, 0, 0)
        else:
            background_color = (255, 255, 255)
            text_color = (0, 0, 0)

        if len(self.image.getbands()) == 4:
            # add alpha channel
            background_color = (*background_color, 255)
            text_color = (*text_color, 255)

        return (
            np.array(background_color, dtype=np.uint8),
            np.array(text_color, dtype=np.uint8)
        )

    def translate_text(self, data: list[OCRData]) -> None:
        """Erases text from the image.

        Args:
            data (list[OCRData]): data returned by pytesseract.image_to_data
        """
        draw = ImageDraw.Draw(self.image)

        # groups of words and coordinates
        groups = []

        block_num, par_num, line_num = 0, 0, 0
        x1, y1, x2, y2 = -1, -1, -1, -1
        word_list = []
        for row in data:
            if (row is not None
                    and row.level == 5
                    and any([s.isalpha() for s in row.text])):

                if (block_num == row.block_num
                        and par_num == row.par_num):

                    if line_num != row.line_num:
                        word_list.append('\n')
                        line_num = row.line_num

                    word_list.append(row.text)
                    if x1 == -1 or x1 > row.left:
                        x1 = row.left
                    if y1 == -1 or y1 > row.top:
                        y1 = row.top
                    if x2 < row.left + row.width:
                        x2 = row.left + row.width
                    if y2 < row.top + row.height:
                        y2 = row.top + row.height
                else:
                    if word_list:
                        block = (x1, y1, x2, y2)
                        _, text_color = self._determine_colors(
                            block
                        )
                        groups.append({
                            'words': word_list,
                            'block': block,
                            'color': tuple(text_color)
                        })
                    block_num = row.block_num
                    par_num = row.par_num
                    line_num = row.line_num
                    x1, y1 = row.left, row.top
                    x2, y2 = row.left + row.width, row.top + row.height
                    word_list = [row.text]
        if word_list:
            block = (x1, y1, x2, y2)
            _, text_color = self._determine_colors(
                block
            )
            groups.append({
                'words': word_list,
                'block': block,
                'color': tuple(text_color)
            })

        # clear image from text
        for row in data:
            if (row is not None
                    and row.level == 5
                    and any([s.isalpha() for s in row.text])):

                back_color, text_color = self._determine_colors((
                    row.left,
                    row.top,
                    row.left + row.width,
                    row.top + row.height
                ))
                self.__clear_block(back_color, (
                    row.left,
                    row.top,
                    row.left + row.width,
                    row.top + row.height
                ))

        # draw text
        for group in groups:

            text = ' '.join(group.get('words'))
            translated_text = self.translator.translate(text)

            block = group.get('block')

            font = self.__get_font(
                draw=draw,
                text=translated_text,
                block=block
            )
            draw.multiline_text(
                xy=(
                    (block[0] + block[2]) / 2,  # x
                    (block[1] + block[3]) / 2   # y
                ),
                text=translated_text,
                font=font,
                fill=group.get('color'),
                anchor='mm',
                align='center',
            )
            # draw.rectangle(xy=block, outline=(255, 0, 0))

    def __clear_block(self, color, block):
        if block[0] > 0 and block[1] > 0:
            cleaning_block = (
                block[0] - 1,
                block[1] - 1,
                block[2],
                block[3]
            )
        else:
            cleaning_block = block

        box = self.image.crop(cleaning_block)
        # create grayscale mask
        mask = box.convert('L').point(
            lambda c: 0 if c > 200 else 255)
        # dilate and blur the mask
        mask = self.__blur(self.__dilate(mask, 2), 2)
        # create the box and fill it with the background color
        box = Image.fromarray(
            np.ones_like(
                box, dtype=np.uint8
            ) * color)
        # erase text
        self.image.paste(
            box,
            cleaning_block,
            mask)

    def __get_font(self, draw: ImageDraw, text: str, block: tuple) -> int:
        size = 14
        font = self.__get_default_font(size)
        for _ in range(100):
            box = draw.multiline_textbbox(
                xy=(block[0], block[1]),
                text=text,
                font=font
            )
            if box[2] > block[2] or box[3] > block[3]:
                size -= 1
            elif ((0 <= (block[2] - box[2]) <= 10)
                    or (0 <= (block[3] - box[3]) <= 10)):
                # the box less then the block within 10 pixels
                # stop search
                break
            else:
                size += 1
            font = self.__get_default_font(size)

        return font

    @staticmethod
    def __get_default_font(size: int):
        return ImageFont.truetype('arial.ttf', size)

    @staticmethod
    def __erode(image, cycles, size=3):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MinFilter(size))
        return image

    @staticmethod
    def __dilate(image, cycles, size=3):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MaxFilter(size))
        return image

    @staticmethod
    def __blur(image, radius=1):
        return image.filter(ImageFilter.BoxBlur(radius))
