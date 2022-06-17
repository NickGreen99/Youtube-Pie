import pytest
from backend.app import app
from flask import session
from backend import authentication
from googleapiclient.discovery import build


@pytest.fixture
def urls():
    url_list = ['/login', '/index']
    return url_list


@pytest.fixture
def client():
    return app.test_client()


def test_get_request(client, urls):
    for url in urls:
        response = client.get(url)
        assert response.status_code == 200




