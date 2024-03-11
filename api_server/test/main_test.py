from fastapi.testclient import TestClient
from fastapi import status

from api_server.src.domain import api
from api_server.src.main import app

client = TestClient(app=app)


def test_root_available():
    """
    """
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK


def test_failed_authentification_without_api_key():
    """
    """
    request = api.ImageToTextRequest(
        image=''
    )

    response = client.post(
        url='/image_to_text',
        json=request.model_dump(),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_failed_authentification_with_wrong_api_key():
    """
    """
    request = api.ImageToTextRequest(
        image=''
    )
    headers = {'X-API-key': 'no'}

    response = client.post(
        url='/image_to_text',
        headers=headers,
        json=request.model_dump(),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
