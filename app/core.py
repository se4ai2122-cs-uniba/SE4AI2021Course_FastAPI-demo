"""Core logic: loading the models and making predictions.

This module knows nothing about HTTP or MCP. Both the FastAPI app (`app/api.py`)
and the MCP server (`app/mcp_server.py`) are thin adapters built on top of it.
"""

import pickle
from enum import Enum
from pathlib import Path

# Resolved from this file's location rather than from the current working directory:
# an MCP client may launch the server from anywhere.
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

# Maps each model type (e.g., "SVC") to its wrapper, as pickled by `scripts/train.py`
model_wrappers: dict[str, dict] = {}


class IrisType(Enum):
    setosa = 0
    versicolor = 1
    virginica = 2


class ModelNotFoundError(LookupError):
    """Raised when a prediction is requested from a model that is not loaded."""


def load_models() -> None:
    """Load all pickled models found in `MODELS_DIR`."""

    for path in sorted(MODELS_DIR.glob("*.pkl")):
        with open(path, "rb") as file:
            model_wrapper = pickle.load(file)
            model_wrappers[model_wrapper["type"]] = model_wrapper


def unload_models() -> None:
    """Discard all loaded models."""

    model_wrappers.clear()


def list_models() -> list[dict]:
    """Describe the loaded models: type, hyperparameters, and accuracy."""

    return [
        {
            "type": model["type"],
            "parameters": model["params"],
            "accuracy": model["metrics"],
        }
        for model in model_wrappers.values()
    ]


def predict(
    model_type: str,
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float,
) -> IrisType:
    """Classify an Iris flower with the requested model."""

    model_wrapper = model_wrappers.get(model_type)

    if model_wrapper is None:
        available = ", ".join(model_wrappers) or "none"
        raise ModelNotFoundError(
            f"Model '{model_type}' not found. Available models: {available}."
        )

    # sklearn's `predict()` methods expect a 2D array of shape [n_samples, n_features]
    # therefore, we need to convert our single data point into a 2D array
    features = [[sepal_length, sepal_width, petal_length, petal_width]]

    prediction = model_wrapper["model"].predict(features)
    return IrisType(int(prediction[0]))
