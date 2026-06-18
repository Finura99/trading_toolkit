from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_trades():
    response = client.get("/trades?limit=1")

    assert response.status_code in [200,404] # checks if whether db has data or is empty

def test_get_trades_invalid_limit_returns_422(): # validation test for invalid query param
    response = client.get("/trades?limit=101")

    assert response.status_code == 422

def test_get_portfolio_missing_symbol_returns_422():
    response = client.get("/portfolio/DOESNOTEXIST")

    assert response.status_code == 404
    assert response.json()["detail"] == "Portfolio position not found"