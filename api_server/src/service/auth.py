import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader


ENV_TOKEN = 'SMART_SNIP_TOKEN'

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
    token = os.getenv(ENV_TOKEN)
    if api_key_header == ('-' if token is None else token):
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or missing API key'
    )
