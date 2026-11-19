"""Main script: it includes our API initialization and endpoints."""

import pickle
from contextlib import asynccontextmanager
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI, Request

from app.schemas import IrisType, PredictPayload

import gradio as gr

MODELS_DIR = Path("models/")
model_wrappers_list: list[dict] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle application lifespan events.

    Used to load all pickled models found in `MODELS_DIR` and add them to `models_list`
    """

    # Load all models
    model_paths = [
        filename for filename in MODELS_DIR.iterdir() if filename.suffix == ".pkl"
    ]

    for path in model_paths:
        # Blocking I/O is fine here: it runs once, before the server accepts requests
        with open(path, "rb") as file:  # noqa: ASYNC230
            model_wrapper = pickle.load(file)
            model_wrappers_list.append(model_wrapper)

    yield

    # Clean up the models list
    model_wrappers_list.clear()


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

    available_models = [
        {
            "type": model["type"],
            "parameters": model["params"],
            "accuracy": model["metrics"],
        }
        for model in model_wrappers_list
    ]

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": available_models,
    }

    return response


def _predict_core(
    type: str,
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float,
) -> tuple[int, str]:
    model_wrapper = next((m for m in model_wrappers_list if m["type"] == type), None)

    # sklearn's `predict()` methods expect a 2D array of shape [n_samples, n_features]
    # therefore, we need to convert our single data point into a 2D array
    features = [
        [
            sepal_length,
            sepal_width,
            petal_length,
            petal_width,
        ]
    ]

    if model_wrapper:
        prediction = model_wrapper["model"].predict(features)
        prediction = int(prediction[0])
        predicted_type = str(IrisType(prediction).name)
        return prediction, predicted_type
    else:
        raise ValueError(f"Model of type '{type}' not found.")


@app.post("/models/{type}", tags=["Prediction"])
@construct_response
def _predict(request: Request, type: str, payload: PredictPayload):
    """Classifies Iris flowers based on sepal and petal sizes."""

    try:
        prediction, predicted_type = _predict_core(
            type=type,
            sepal_length=payload.sepal_length,
            sepal_width=payload.sepal_width,
            petal_length=payload.petal_length,
            petal_width=payload.petal_width,
        )

        response = {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": {
                "model-type": type,
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
    except ValueError as e:
        response = {
            "message": str(e),
            "status-code": HTTPStatus.BAD_REQUEST,
        }
        return response


inputs = [
    gr.Dropdown(["LogisticRegression", "SVC"], label="Model Type", value="SVC"),
    gr.Number(label="Sepal Length", value=6.4),
    gr.Number(label="Sepal Width", value=2.8),
    gr.Number(label="Petal Length", value=5.6),
    gr.Number(label="Petal Width", value=2.1),
]
outputs = [
    gr.Textbox(label="Predicted Class (0: setosa, 1: versicolor, 2: virginica)"),
    gr.Textbox(label="Predicted Class Name"),
]
gradio_interface = gr.Interface(
    title="Iris Flower Classifier",
    description="Classifies Iris flowers based on sepal and petal sizes using a selected model.",
    fn=_predict_core,
    inputs=inputs,
    outputs=outputs,
    article="""
    <p>This Gradio interface allows you to classify Iris flowers based on their sepal and petal sizes using a selected machine learning model.</p>
    <p>Choose a model type from the dropdown, enter the sepal and petal dimensions, and click 'Submit' to see the predicted class and its name.</p>
    <p>Model Types:</p>
    <ul>
        <li><strong>LogisticRegression</strong>: A linear model for classification.</li>
        <li><strong>SVC</strong>: Support Vector Classifier, a powerful model for classification tasks.</li>
    </ul> """,
)
app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")
