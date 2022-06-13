import pytest
from backend.app import app


@pytest.fixture
def urls():
    url_list = ['/login', '/index']
    return url_list


@pytest.fixture
def client():
    return app.test_client()


def test_urls(client, urls):
    for url in urls:
        response = client.get(url)
        # assert response.get_data() == b'Hello,World'
        assert response.status_code == 200
