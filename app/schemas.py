"""Definitions for the objects used by our resource endpoints."""

from enum import Enum

from pydantic import BaseModel


class PredictPayload(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    class Config:
        # The json_schema_extra option can be used to add extra information to the JSON schema
        json_schema_extra = {
            "example": {
                "sepal_length": 6.4,
                "sepal_width": 2.8,
                "petal_length": 5.6,
                "petal_width": 2.1,
            }
        }


class IrisType(Enum):
    setosa = 0
    versicolor = 1
    virginica = 2
