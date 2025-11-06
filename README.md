# FastAPI Lab

This demo project, developed for the Software Engineering for AI-enabled Systems course at the University of Bari (Department of Computer Science), demonstrates how to serve machine learning models using FastAPI.

The scripts in this project are freely inspired by the [Made with ML](https://madewithml.com) tutorial: "[APIs for Machine Learning](https://madewithml.com/courses/mlops/api/)".

## Project setup

Install all project requirements with `uv`:

```bash
uv sync
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
  print (json.loads(response.text))
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
