from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_stock():
    response = client.post("/stocks",json={"symbol": "AMZN", "name": "AMAZON", "price": 13.98})

    assert response.status_code == 200
    assert response.json() == {"stock": "Added AMAZON"}


def test_get_all_stocks():
    response = client.get("/stocks")

    assert response.status_code == 200

def test_get_stock_not_found():
    response = client.get("/stocks/Nope")

    assert response.status_code == 404
    assert response.json() == {"detail":"Symbol not found"}