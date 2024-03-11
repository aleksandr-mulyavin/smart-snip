import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name='X-API-key')


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Checks the value of the API key.

    Args:
        api_key_header (str, optional): API key from header.
          Defaults to Security(api_key_header).

    Raises:
        HTTPException: status 401

    Returns:
        str: API key
    """
    if api_key_header == os.getenv('SMART_SNIP_TOKEN'):
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or missing API key'
    )
