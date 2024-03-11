from pydantic import BaseModel


class ImageToTextRequest(BaseModel):
    image: str
    lang: str = ''


class Error(BaseModel):
    error: str
