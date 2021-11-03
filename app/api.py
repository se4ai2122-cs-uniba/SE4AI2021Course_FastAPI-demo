"""Main script: it includes our API initialization and endpoints."""

from functools import wraps
from datetime import datetime
from http import HTTPStatus
from fastapi import FastAPI, Request


# Define application
app = FastAPI(
    title="Housing Prices Regressor",
    description="Predicts the sale price of a house given the array of its numeric features.",
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
def load_artifacts():
    global model
    pass


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
