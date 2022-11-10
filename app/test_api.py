from fastapi.testclient import TestClient

from .api import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["method"] == "GET"
    assert (
        response.json()["data"]["message"]
        == "Welcome to IRIS classifier! Please, read the `/docs`!"
    )


def test_logreg_model_endpoint():
    """Test the logreg model endpoint."""

    response = client.post(
        "/models/SVC",
        headers={"Content-Type": "application/json"},
        json={
            "sepal_length": 6.4,
            "sepal_width": 2.8,
            "petal_length": 5.6,
            "petal_width": 2.1,
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["predicted_type"] == "virginica"
