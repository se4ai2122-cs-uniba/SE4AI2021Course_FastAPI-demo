"""MCP server: it exposes our models as tools that an LLM agent can call.

Unlike a REST endpoint, a tool is "read" by a language model, not by a programmer:
its name, its docstring, and the descriptions of its parameters are all the model
knows when deciding whether and how to call it. Write them as you would a prompt.
"""

from contextlib import asynccontextmanager
from typing import Annotated, Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from app import core, images


@asynccontextmanager
async def lifespan(server: MCPServer):
    """Load all pickled models at startup and discard them at shutdown."""

    core.load_models()

    yield

    core.unload_models()


# Define the server
mcp = MCPServer(
    name="iris-classifier",
    instructions=(
        "Classifies Iris flowers into species, based on sepal and petal sizes. "
        "Also reports the basic properties of an image, given its path or URL."
    ),
    lifespan=lifespan,
)


@mcp.tool()
def list_models() -> list[dict]:
    """List the models available to classify Iris flowers.

    For each model, returns its type, its hyperparameters, and its accuracy
    (estimated by cross-validation). Useful to choose the model for `predict_iris`.
    """

    return core.list_models()


@mcp.tool()
def predict_iris(
    # A `Literal` lists the allowed values in the tool's schema, so the LLM cannot
    # invent a model name. Keep it in sync with the models trained in `scripts/train.py`
    model_type: Annotated[
        Literal["LogisticRegression", "SVC"],
        Field(description="The model to use for the prediction"),
    ],
    sepal_length: Annotated[float, Field(description="Sepal length, in cm", gt=0)],
    sepal_width: Annotated[float, Field(description="Sepal width, in cm", gt=0)],
    petal_length: Annotated[float, Field(description="Petal length, in cm", gt=0)],
    petal_width: Annotated[float, Field(description="Petal width, in cm", gt=0)],
) -> dict:
    """Predict the species of an Iris flower from the sizes of its sepals and petals.

    Returns the predicted species: setosa, versicolor, or virginica.
    """

    try:
        iris_type = core.predict(
            model_type, sepal_length, sepal_width, petal_length, petal_width
        )
    except core.ModelNotFoundError as error:
        # A `ToolError` is reported to the LLM as a failed tool call, with this message
        raise ToolError(str(error)) from error

    return {"model_type": model_type, "predicted_species": iris_type.name}


@mcp.tool()
def get_image_info(
    # The arguments of a tool call are JSON written by the LLM, and an LLM cannot
    # copy the bytes of an image attached to the chat into them. So the image is
    # passed by reference: the LLM writes where the image is, and the server
    # fetches it. A local path works because this server runs on the user's machine
    image: Annotated[
        str,
        Field(
            description="Absolute path of an image file on this computer, "
            "or an http(s) URL of an image"
        ),
    ],
) -> dict:
    """Report the basic properties of an image.

    Returns its format, width and height in pixels, color mode, resolution (DPI,
    when the file stores it), and size in bytes.
    """

    try:
        return images.describe_image(image)
    except images.ImageLoadError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    # Communicate over stdio (the default transport): the MCP client launches
    # this script as a subprocess and talks to it via stdin/stdout
    mcp.run()
