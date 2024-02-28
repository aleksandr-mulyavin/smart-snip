from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import service
from domain import api

logger = service.get_logger(__name__)

app = FastAPI()


@app.get('/')
async def root() -> str:
    """Root handler.

    Returns:
        str: return string 'OCR API'
    """
    return 'OCR API'


@app.post('/image_to_text')
async def image_to_text(request: api.ImageToTextRequest) -> JSONResponse:
    """Handler for image_to_text method.

    Parameters:
        request (api.ImageToTextRequest):

    Returns:
        JSONResponse: response in JSON format.
    """

    # авторизация по токену
    if not service.check_token(request.api_key):
        # если не прошла, то вернем ошибку 401
        logger.error('Authentication failed')
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=api.Error(error='authentication failed').model_dump()
        )
