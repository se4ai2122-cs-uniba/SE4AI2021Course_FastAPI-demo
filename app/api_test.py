"""Test the API endpoints using FastAPI's TestClient."""

import json

from fastapi.testclient import TestClient

from .api import app


def test_root():
    """Test the root endpoint."""

    with TestClient(app) as client:

        response = client.get("/")

        assert response.status_code == 200

        assert response.json()["method"] == "GET"
        assert response.json()["message"] == "OK"
        assert response.json()["status-code"] == 200
        assert response.json()["timestamp"] is not None

        assert (
            response.json()["data"]["message"]
            == "Welcome to IRIS classifier! Please, read the `/docs`!"
        )


def test_get_model_list():
    """Test the /models endpoint."""

    with TestClient(app) as client:

        response = client.get("/models")

        assert response.status_code == 200

        assert response.json()["method"] == "GET"
        assert response.json()["message"] == "OK"
        assert response.json()["status-code"] == 200
        assert response.json()["timestamp"] is not None

        model_types = [model["type"] for model in response.json()["data"]]
        assert "LogisticRegression" in model_types
        assert "SVC" in model_types
