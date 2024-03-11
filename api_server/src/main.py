from fastapi import FastAPI, Security, status
from fastapi.responses import JSONResponse

from .service import auth, logging
from .domain import api

logger = logging.get_logger(__name__)

app = FastAPI()


@app.get('/')
async def root() -> str:
    """Root handler.

    Returns:
        str: return string 'OCR API'
    """
    return 'OCR API'


@app.post('/image_to_text')
async def image_to_text(
    request: api.ImageToTextRequest,
    api_key: str = Security(auth.get_api_key)
) -> JSONResponse:
    """Handler for image_to_text method.

    Parameters:
        request (api.ImageToTextRequest):

    Returns:
        JSONResponse: response in JSON format.
    """
    return JSONResponse(
        content='',
        status_code=status.HTTP_200_OK,
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
