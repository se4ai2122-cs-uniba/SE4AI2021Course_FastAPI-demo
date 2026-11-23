"""Definitions for the objects used by our resource endpoints."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PredictPayload(BaseModel):
    sepal_length: Annotated[float, Field(description="Sepal length, in cm", gt=0)]
    sepal_width: Annotated[float, Field(description="Sepal width, in cm", gt=0)]
    petal_length: Annotated[float, Field(description="Petal length, in cm", gt=0)]
    petal_width: Annotated[float, Field(description="Petal width, in cm", gt=0)]

    model_config = ConfigDict(
        # The json_schema_extra option can be used to add extra information to the JSON schema
        json_schema_extra={
            "example": {
                "sepal_length": 6.4,
                "sepal_width": 2.8,
                "petal_length": 5.6,
                "petal_width": 2.1,
            }
        }
    )
