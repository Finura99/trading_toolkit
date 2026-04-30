from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_trades():
    response = client.get("/trades?limit=1")

    assert response.status_code in [200,404] # checks if whether db is empty or has data