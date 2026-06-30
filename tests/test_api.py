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
    assert response.json()["detail"] == "Portfolio position not found" # more tests can be added for other endpoints and scenarios as needed

def test_get_positions():
    response = client.get("/positions")

    assert response.status_code == 200 # 200 HTTP means /positions endpoint exists

    data = response.json() # convert the json response into python data

    assert isinstance(data, list) # check the response is a list
    assert len(data) > 0 # check if item has alteast 1 item

    first_position = data[0] # access the first element of the list item

    assert "symbol" in first_position
    assert "net_quantity" in first_position 
    assert "market_price" in first_position
    assert "exposure" in first_position
    # each position has symbol, net quantity, market_price and exposure...

