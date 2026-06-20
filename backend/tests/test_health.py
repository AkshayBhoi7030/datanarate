import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "version" in data["data"]
    assert "name" in data["data"]
