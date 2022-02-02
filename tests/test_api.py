import pytest

from api.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_all_news(client):
    assert client.get("/all", query_string={"page": 1}).status_code == 200
    assert client.get("/all", query_string={"page": "0"}).status_code == 400
    assert client.get("/all", query_string={"page": ""}).status_code == 400


def test_search(client):
    assert client.get("/search").status_code == 200


def test_health(client):
    assert client.get("/health").status_code == 200
