# FastAPI and MCP Lab

This demo project, developed for the Software Engineering for AI-enabled Systems course at the University of Bari (Department of Computer Science), demonstrates how to serve machine learning models using FastAPI, and how to expose them as tools for LLM agents via the [Model Context Protocol](https://modelcontextprotocol.io) (MCP).

The scripts in this project are freely inspired by the [Made with ML](https://madewithml.com) tutorial: "[APIs for Machine Learning](https://madewithml.com/courses/mlops/api/)".

## Project setup

Install all project requirements with `uv`:

```bash
uv sync
```

## (Optional) Retrain the models

The `models/` folder already contains two pickled models. Pickles are tied to the scikit-learn version that produced them, so if you upgrade scikit-learn, regenerate them:

```bash
uv run python scripts/train.py
```

## Launch the server

Use the FastAPI CLI via `uv` to launch the application in development mode (with auto-reload):

```bash
uv run fastapi dev app/api.py
```

In detail:

- `fastapi dev` runs a development server with auto-reload;
- `app/api.py` is the entrypoint module for the app;
- You can pass `--host` and `--port` to customize bind address and port (defaults are `127.0.0.1:8000`).

**Observation**. For production, prefer an ASGI server setup (e.g., `uvicorn` or `gunicorn` with multiple `uvicorn` workers). The `fastapi dev` command is intended for development only.

## Try the API

We can now test that the application is working. These are some of the possibilities:

- visit [localhost:8000](http://localhost:8000/)
- use `curl`

  ```bash
  curl -X GET http://localhost:8000/
  ```

- access the API programmatically, e.g.:

  ```python
  import json
  import requests

  response = requests.get("http://localhost:8000/")
  print(json.loads(response.text))
  ```

- use an external tool like [Postman](https://www.postman.com), which lets you execute and manage tests that can be saved and shared with others.

### Accessing the documentation

We can access the [Swagger UI](https://swagger.io/tools/swagger-ui/) for our documentation by going to the `/docs` endpoint. Alternatively, the documentation generated via [Redoc](https://github.com/Redocly/redoc) is accessible at the `/redoc` endpoint.

### Requests to try

#### Virginica (2)

```json
{
  "sepal_length": 6.4,
  "sepal_width": 2.8,
  "petal_length": 5.6,
  "petal_width": 2.1
}
```

#### Setosa (0)

```json
{
  "sepal_length": 5.7,
  "sepal_width": 3.8,
  "petal_length": 1.7,
  "petal_width": 0.3
}
```

## Expose the models as MCP tools

The same models can be called by an LLM agent through the [Model Context Protocol](https://modelcontextprotocol.io). The project is organized so that the web API and the MCP server are two thin adapters over the same core logic:

| Module              | Role                                                             |
| ------------------- | ---------------------------------------------------------------- |
| `app/core.py`       | Loads the models and makes predictions; knows no protocol        |
| `app/api.py`        | Exposes the core as REST endpoints (FastAPI)                     |
| `app/mcp_server.py` | Exposes the core as MCP tools (official `mcp` Python SDK)        |

The MCP server offers two tools: `list_models` and `predict_iris`.

**Observation**. A REST endpoint is read by a programmer; a tool is read by a language model. The tool's name, its docstring, and the descriptions of its parameters are all the model knows when deciding whether and how to call it, so they should be written with the same care as a prompt.

### Launch the MCP server

```bash
uv run python -m app.mcp_server
```

The server communicates over _stdio_: it waits for JSON-RPC messages on standard input, so launching it by hand shows nothing. Normally it is the MCP client (e.g., LM Studio) that launches it as a subprocess.

### Inspect the tools

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) plays the role that Swagger UI plays for the web API: it lists the tools with their schemas and lets us call them by hand (it requires Node.js).

```bash
npx @modelcontextprotocol/inspector uv run python -m app.mcp_server
```

### Call the tools programmatically

```python
import asyncio

from mcp import Client, StdioServerParameters

server = StdioServerParameters(
    command="uv", args=["run", "python", "-m", "app.mcp_server"]
)


async def main():
    async with Client(server) as client:
        result = await client.call_tool(
            "predict_iris",
            {
                "model_type": "SVC",
                "sepal_length": 6.4,
                "sepal_width": 2.8,
                "petal_length": 5.6,
                "petal_width": 2.1,
            },
        )
        print(result.content[0].text)


asyncio.run(main())
```

### Use the tools from LM Studio

1. In [LM Studio](https://lmstudio.ai), load a model that supports tool calling.
2. Open the `mcp.json` file (_Program_ tab → _Install_ → _Edit mcp.json_) and add the server, replacing the path with the absolute path of this repository:

   ```json
   {
     "mcpServers": {
       "iris-classifier": {
         "command": "uv",
         "args": [
           "--directory",
           "/absolute/path/to/this/repository",
           "run",
           "python",
           "-m",
           "app.mcp_server"
         ]
       }
     }
   }
   ```

   If LM Studio cannot find `uv`, use its absolute path as the command (find it with `which uv`).

3. Enable the `iris-classifier` server in the chat and try a prompt such as:

   > I measured an iris flower: the sepal is 6.4 cm long and 2.8 cm wide, the petal is 5.6 cm long and 2.1 cm wide. Which species is it? Use the most accurate model available.
