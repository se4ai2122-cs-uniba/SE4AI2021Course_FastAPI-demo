"""Main script: it includes our API initialization and endpoints."""

from contextlib import asynccontextmanager
from datetime import datetime
from functools import wraps
from http import HTTPStatus

from fastapi import FastAPI, Request

from app import core
from app.schemas import PredictPayload


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle application lifespan events.

    Used to load all pickled models at startup and to discard them at shutdown.
    """

    core.load_models()

    yield

    core.unload_models()


# Define application
app = FastAPI(
    title="Yet another Iris example",
    description="This API lets you make predictions on the Iris dataset using a couple of simple models.",
    version="0.1",
    lifespan=lifespan,
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
            "url": str(request.url),
        }

        # Add data
        if "data" in results:
            response["data"] = results["data"]

        return response

    return wrap


@app.get("/", tags=["General"])  # path operation decorator
@construct_response
def _index(request: Request):
    """Root endpoint."""

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {"message": "Welcome to IRIS classifier! Please, read the `/docs`!"},
    }
    return response


@app.get("/models", tags=["Prediction"])
@construct_response
def _get_models_list(request: Request):
    """Return the list of available models"""

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": core.list_models(),
    }

    return response


@app.post("/models/{type}", tags=["Prediction"])
@construct_response
def _predict(request: Request, type: str, payload: PredictPayload):
    """Classifies Iris flowers based on sepal and petal sizes."""

    features = payload.model_dump()

    try:
        iris_type = core.predict(type, **features)
    except core.ModelNotFoundError:
        return {
            "message": "Model not found",
            "status-code": HTTPStatus.BAD_REQUEST,
        }

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            "model-type": type,
            "features": features,
            "prediction": iris_type.value,
            "predicted_type": iris_type.name,
        },
    }
