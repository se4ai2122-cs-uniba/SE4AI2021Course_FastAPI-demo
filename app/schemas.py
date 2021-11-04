"""Definitions for the objects used in our resource endpoints."""

from pydantic import BaseModel
from enum import Enum


class PredictPayload(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class IrisType(Enum):
    setosa = 0
    versicolor = 1
    virginica = 2
