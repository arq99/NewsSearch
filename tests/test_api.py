import json
import pytest
from api.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_all_news(client):
    assert client.get("/allnews").status_code == 200


def test_search(client):
    assert client.post("/search", query_string={'query': 'Technology'}).status_code == 200


def test_health(client):
    assert client.get("/health").status_code == 200
