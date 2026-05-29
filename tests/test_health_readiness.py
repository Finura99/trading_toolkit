from unittest.mock import patch
from fastapi.testclient import TestClient

from src.main import app ## stateless application

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_readiness_returns_ready_when_database_connected():
    with patch("src.main.check_db_connection", return_value=True): # mock data ?
        response = client.get("/readiness")

    assert response.status_code == 200
    assert response.json() == {"status": "ok",
                            "database": "active"}
    

def test_readiness_returns_503_when_database_unavailable():
    with patch("src.main.check_db_connection", return_value=False):
        response = client.get("/readiness")

    assert response.status_code == 503
    assert response.json()["detail"] == {"status": "not_ready",
                                        "database": "unavailable"}