from pydantic import BaseModel

from ..service.logging import get_logger

__logger = get_logger(__name__)


class OCRData(BaseModel):
    """Class of a recognized text block
    """
    level: int
    page_num: int
    block_num: int
    par_num: int
    line_num: int
    word_num: int
    left: int
    top: int
    width: int
    height: int
    conf: float
    text: str

    @staticmethod
    def from_str(string: str):
        """The function to create an instance of the class from a string.
        """
        row = [x for x in string.split('\t')]
        if len(row) == 12:
            try:
                return OCRData(
                    level=int(row[0]),
                    page_num=int(row[1]),
                    block_num=int(row[2]),
                    par_num=int(row[3]),
                    line_num=int(row[4]),
                    word_num=int(row[5]),
                    left=int(row[6]),
                    top=int(row[7]),
                    width=int(row[8]),
                    height=int(row[9]),
                    conf=float(row[10]),
                    text=row[11],
                )
            except ValueError as e:
                __logger.error(f'{str(e)}:\n{row}')
        else:
            __logger.error(
                'the number of elements in the string '
                f'is not equal to 12 :\n{row}'
            )
        return None
