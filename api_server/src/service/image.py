import numpy as np
from sklearn.cluster import KMeans
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont
)

from ..domain.ocr import OCRData


class ImageHandler():
    """Class for image processing: erase text, draw text.
    """
    def __init__(self, image: Image):
        self.image = image
        self.primary_color = (255, 255, 255)
        self.primary_color_array = np.array(self.primary_color)

    def determine_backround_color(self) -> None:
        """Determines the background color of the image using KMeans.
        """
        # prepare image for KMeans
        bands = self.image.split()
        rgb = [np.asarray(band).flatten() for band in bands[:4]]
        reshape = np.array(
            [[rgb[0][i], rgb[1][i], rgb[2][i]] for i in range(rgb[0].shape[0])]
        )
        cluster = KMeans(n_clusters=5).fit(reshape)

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
        primary_color = colors[0][1]
        if len(self.image.getbands()) == 4:
            primary_color = (*primary_color, 255)
        self.primary_color = primary_color
        self.primary_color_array = np.array(primary_color, dtype=np.uint8)

    def erase_text(self, data: list[OCRData]) -> None:
        """Erases text from the image.

        Args:
            data (list[OCRData]): data returned by pytesseract.image_to_data
        """
        self.determine_backround_color()

        for row in data:
            if row is not None and row.conf != -1:

                if row.text.strip() != '':

                    x = row.left
                    y = row.top
                    width = row.width
                    height = row.height

                    if width > 5 and height > 5:
                        box = self.image.crop(
                            (x, y, x + width, y + height))
                        mask = box.convert('L').point(
                            lambda c: 0 if c > 200 else 255)
                        mask = ImageHandler.__blur(
                            ImageHandler.__dilate(mask, 1))
                        box = Image.fromarray(
                            np.ones_like(
                                box, dtype=np.uint8
                            ) * self.primary_color_array)
                        self.image.paste(
                            box,
                            (x, y, x + width, y + height),
                            mask)

    def draw_text(self, data: list[OCRData]) -> None:
        font = ImageFont.truetype('arial.ttf', 30)
        draw = ImageDraw.Draw(self.image)

        for row in data:
            if row is not None and row.conf != -1:
                if row.text.strip() != '':
                    if row.width > 10 and row.height > 10:
                        draw.text(
                            xy=(row.left, row.top),
                            text=row.text,
                            font=font,
                            fill=(0, 0, 0)
                        )

    @staticmethod
    def __erode(image, cycles):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MinFilter(3))
        return image

    @staticmethod
    def __dilate(image, cycles):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MaxFilter(3))
        return image

    @staticmethod
    def __blur(image, radius=1):
        return image.filter(ImageFilter.BoxBlur(radius))
