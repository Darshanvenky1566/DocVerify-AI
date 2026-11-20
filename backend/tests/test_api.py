import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "DocVerify AI",
    }


def test_home_redirects_to_swagger():
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/docs"


@pytest.mark.parametrize(
    "path",
    [
        "/applications",
        "/reviews/queue",
        "/reviews/2/documents",
        "/reviews/2/documents/2/download",
    ],
)
def test_protected_routes_require_login(path):
    response = client.get(path)

    assert response.status_code == 401