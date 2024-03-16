from pydantic import BaseModel

from ..service.logging import get_logger

logger = get_logger(__name__)


class OCRData(BaseModel):
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
                logger.error(f'{str(e)}:\n{row}')
        else:
            logger.error(
                'the number of elements in the string '
                f'is not equal to 12 :\n{row}'
            )
        return None
