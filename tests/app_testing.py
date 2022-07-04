import pytest
import sys

sys.path.insert(1, '../backend')

from backend.app import app, percentages


# pytest annotations
@pytest.fixture
def webapp_urls():
    url_list = ['/']
    return url_list


@pytest.fixture
def oauth_urls():
    url_list = ['/authorize', '/clear', '/stats']
    return url_list


@pytest.fixture
def client():
    return app.test_client()


# test for get response with status code 200 (OK)
def test_webapp_get_request(client, webapp_urls):
    for url in webapp_urls:
        response = client.get(url)
        assert response.status_code == 200


# test for get response with status code 302 (Redirect)
def test_oauth_get_request(client, oauth_urls):
    for url in oauth_urls:
        response = client.get(url)
        assert response.status_code == 302


# test that percentages function works properly
def test_percentages():
    categories = ['Gaming', 'Movies', 'Gaming']
    labels, sizes, colors = percentages(categories)
    assert len(labels) == 2
    assert len(sizes) == 2
    print(sizes)
    assert round(sizes[0], 1) == 66.7
    assert round(sizes[1], 1) == 33.3
