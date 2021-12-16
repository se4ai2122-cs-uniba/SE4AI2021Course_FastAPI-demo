# FastAPI Lab

This is a demo project used to show how to serve ML models with FastAPI in the 2021 edition of the Software Engineering for AI-enabled Systems course (University of Bari, Italy - Dept. of Computer Science).

The scripts in this project are freely inspired by the [Made with ML](https://madewithml.com) tutorial: "[APIs for Machine Learning](https://madewithml.com/courses/mlops/api/)".

## Project setup

Install all project requirements with `pip`:

```bash
pip install -r requirements.txt
```

## Launch the server

We'll be using Uvicorn, a fast ASGI server (it can run asynchronous code in a single process) to launch our application. `cd` to the `app/` directory and use the following command to start the server:

```bash
uvicorn api:app \
    --host 0.0.0.0 \
    --port 5000 \
    --reload
```

In detail:

- `uvicorn app.api:app` is the location of app (`app` directory > `api.py` script > `app` object);
- `--reload` makes the server reload every time we update;
- `--reload-dir app` makes it only reload on updates to the `app/` directory;
- `--reload-dir models` makes it also reload on updates to the `models/` directory;

**Observation**. If we want to manage multiple `uvicorn` workers to enable parallelism in our application, we can use **Gunicorn** in conjunction with **Uvicorn**.

## Try the API

We can now test that the application is working. These are some of the possibilities:

- visit [localhost:5000](http://localhost:5000/)
- use `curl`

  ```bash
  curl -X GET http://localhost:5000/
  ```

- access the API programmatically, e.g.:

  ```python
  import json
  import requests

  response = requests.get("http://localhost:5000/")
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
