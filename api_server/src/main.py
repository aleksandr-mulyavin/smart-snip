from fastapi import FastAPI, Security, status
from fastapi.responses import JSONResponse

from .service import auth, logging, ocr
from .domain.api import (
    ImageToTextRequest,
    ImageToDataResponse,
    TranslateImageTextRequest,
    TranslateImageTextResponse
)

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
    request: ImageToTextRequest,
    api_key: str = Security(auth.get_api_key)
) -> JSONResponse:
    """Handler for image_to_text method.

    Parameters:
        request (ImageToTextRequest):

    Returns:
        JSONResponse: response in JSON format.
    """
    text = ocr.image_to_string(
        request.image,
        request.lang,
    )

    return JSONResponse(
        content=text,
        status_code=status.HTTP_200_OK,
    )


@app.post('/image_to_data')
async def image_to_data(
    request: ImageToTextRequest,
    api_key: str = Security(auth.get_api_key)
) -> ImageToDataResponse:
    """Handler for image_to_data method.

    Parameters:
        request (ImageToTextRequest):

    Returns:
        ImageToDataResponse: response in JSON format.
    """
    ocr_data = ocr.image_to_data(
        request.image,
        request.lang,
    )

    return JSONResponse(
        content=ImageToDataResponse(
            image_data=ocr_data
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@app.post('/translate_image_text')
async def translate_image_text(
    request: TranslateImageTextRequest,
    api_key: str = Security(auth.get_api_key)
) -> TranslateImageTextResponse:
    """Handler for translate_image_text method.

    Parameters:
        request (TranslateImageTextRequest):

    Returns:
        TranslateImageTextResponse: contains image with translated text.
    """
    result = TranslateImageTextResponse(
        image=ocr.translate_image_text(
                    request.image,
                    request.to_lang)
    )

    return JSONResponse(
        content=result.model_dump(),
        status_code=status.HTTP_200_OK,
    )


@app.get('/languages')
async def get_languages(
    api_key: str = Security(auth.get_api_key)
) -> JSONResponse:
    """Handler for method get_languages.

    Args:
        api_key_header (str, optional): API key from header.
          Defaults to Security(api_key_header).

    Returns:
        JSONResponse: list of supported languages
    """
    return JSONResponse(
        content=ocr.get_languages(),
        status_code=status.HTTP_200_OK,
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
