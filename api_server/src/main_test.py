from fastapi.testclient import TestClient
from fastapi import status

from domain import api
from main import app

client = TestClient(app=app)


def test_root_available():
    """
    """
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK


def test_failed_authentification():
    """
    """
    request = api.ImageToTextRequest(
        api_key='',
        image=''
    )

    response = client.post(
        url='/image_to_text',
        json=request.model_dump()
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
