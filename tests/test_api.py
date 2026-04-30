from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_trades():
    response = client.get("/trades?limit=1")

    assert response.status_code == 200 # checks if its a 200
    assert isinstance(response.json(), list) # checks if its a 