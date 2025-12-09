import pytest
from app import app

def test_hello():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello!" in response.data


def test_health():
    client = app.test_client()
    response = client.get('/health')

    # /health 주소로 찔렀을 때 200이 나오면 서버는 멀쩡한 것임
    assert response.status_code == 200
    assert response.json['status'] == 'ok'