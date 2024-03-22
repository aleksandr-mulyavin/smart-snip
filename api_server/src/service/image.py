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

        for row in data:
            if row is not None and row.conf != -1:

                if row.text.strip() != '':

                    if (row.width > 10
                            and row.height > 5
                            and row.conf > 15
                            and any([s.isalpha() for s in row.text])):

                        text = self.translator.translate(row.text)
                        logger.info(text)

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

                        font = self.__get_font(draw, text, row.width)

                        draw.text(
                            xy=(row.left, row.top),
                            text=text,
                            font=font,
                            fill=tuple(text_color)
                        )

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

    def __get_font(self, draw: ImageDraw, text: str, width: int) -> int:
        size = 14
        font = ImageFont.load_default(size)
        for _ in range(100):
            lenght = draw.textlength(text, font)
            if 0 <= (width - lenght) < 10:
                break
            if lenght > width:
                if size < 5:
                    break
                size -= 1
            else:
                size += 1
            font = ImageFont.load_default(size)

        return font

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
