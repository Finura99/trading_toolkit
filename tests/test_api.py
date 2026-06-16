from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_trades():
    response = client.get("/trades?limit=1")

    assert response.status_code in [200,404] # checks if whether db has data or is empty

def test_get_trades_invalid_limit_returns_422():
    response = client.get("/trades?limit=101")

    assert response.status_code == 422