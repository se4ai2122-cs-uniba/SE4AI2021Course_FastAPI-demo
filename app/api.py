"""Main script: it includes our API initialization and endpoints."""

import pickle

from typing import Dict
from functools import wraps
from datetime import datetime
from http import HTTPStatus
from fastapi import FastAPI, Request
from app.schemas import PredictPayload, IrisType


# Define application
app = FastAPI(
    title="Yet another Iris example",
    description="Making predictions on the Iris dataset using logistic regression.",
    version="0.1",
)


def construct_response(f):
    """Construct a JSON response for an endpoint's results."""

    @wraps(f)
    def wrap(request: Request, *args, **kwargs):
        results = f(request, *args, **kwargs)

        # Construct response
        response = {
            "message": results["message"],
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }

        # Add data
        if "data" in results:
            response["data"] = results["data"]

        return response

    return wrap


@app.on_event("startup")
def load_model():
    global model

    Pkl_Filename = "models/Pickle_RL_Model.pkl"
    with open(Pkl_Filename, "rb") as file:
        model = pickle.load(file)


@app.get("/", tags=["General"])  # path operation decorator
@construct_response
def _index(request: Request):
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response


@app.post("/predict", tags=["Prediction"])
@construct_response
def _predict(request: Request, payload: PredictPayload):
    """Predicts sale price for a house given its numerical features."""

    # sklearn's `predict()` methods expect a 2D array of shape [n_samples, n_features]
    # therefore, we need to convert our single data point into a 2D array
    features = [
        [
            payload.sepal_length,
            payload.sepal_width,
            payload.petal_length,
            payload.petal_width,
        ]
    ]

    prediction = model.predict(features)
    prediction = int(prediction[0])
    predicted_type = IrisType(prediction).name

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            "features": {
                "sepal_length": payload.sepal_length,
                "sepal_width": payload.sepal_width,
                "petal_length": payload.petal_length,
                "petal_width": payload.petal_width,
            },
            "prediction": prediction,
            "predicted_type": predicted_type,
        },
    }
    return response
