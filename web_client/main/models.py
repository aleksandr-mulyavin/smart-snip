from django.db import models
from pydantic import BaseModel


# Create your models here.
class TranslateImageTextRequest(BaseModel):
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    image: str
