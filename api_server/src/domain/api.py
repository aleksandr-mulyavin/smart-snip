from pydantic import BaseModel


class Auth(BaseModel):
    api_key: str


class ImageToTextRequest(Auth):
    image: str


class Error(BaseModel):
    error: str
