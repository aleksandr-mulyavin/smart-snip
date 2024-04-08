from pydantic import BaseModel


class APIConfig(BaseModel):
    url: str
    token: str
    image_to_text: str
    translate_image: str


class ImageToTextRequest(BaseModel):
    image: str
    lang: str = ''


class TranslateImageTextRequest(BaseModel):
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    image: str
