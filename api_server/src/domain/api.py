from pydantic import BaseModel


class ImageToTextRequest(BaseModel):
    image: str


class Error(BaseModel):
    error: str
