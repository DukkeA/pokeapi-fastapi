from fastapi.testclient import TestClient


def test_create_item(client: TestClient) -> None:
    response = client.get("/api/v1/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1017


def test_create_item_2(client: TestClient) -> None:
    response = client.get("/api/v1/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1017


def test_create_item_3(client: TestClient) -> None:
    response = client.get("/api/v1/pokemon/100/")
    assert response.status_code == 200
    data = response.json()
    assert data == 1017
