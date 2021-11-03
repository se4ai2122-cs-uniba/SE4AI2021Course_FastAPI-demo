# FastAPI Lab

Reference tutorial: [APIs for Machine Learning - Made with ML](https://madewithml.com/courses/mlops/api/)

## How to launch the server

We'll be using Uvicorn, a fast ASGI server (it can run asynchronous code in a single process) to launch our application.

```bash
uvicorn app.api:app \       # location of app (`app` directory > `api.py` script > `app` object)
    --host 0.0.0.0 \        # localhost
    --port 5000 \           # port 5000
    --reload \              # reload every time we update
    --reload-dir models \   # only reload on updates to `models` directory
    --reload-dir app        # and the `app` directory
```

**Observation**. If we want to manage multiple uvicorn workers to enable parallelism in our application, we can use Gunicorn in conjunction with Uvicorn.

---

We can now test that the application is working:

- visit [localhost:5000](http://localhost:5000/) in the browser;
- use `curl`
  ```
  curl -X GET http://localhost:5000/
  ```
- access the endpoint via code. E.g.,
  ```python
  import json
  import requests

  response = requests.get("http://localhost:5000/")
  print (json.loads(response.text))
  ```
- use an external tool like [Postman](https://www.postman.com), which lets you execute and manage tests that can be saved and shared with others.


### Accessing the documentation

We can access the [Swagger UI](https://swagger.io/tools/swagger-ui/) for our documentation by going to the `/docs` endpoint. Alternatively, the documentation generated via [Redoc](https://github.com/Redocly/redoc) is accessible at the `/redoc` endpoint.

## Step by step guide

- Basic repo setup
    - .gitignore
    - git init and first commit
- Create the repo structure
  ```
  models/
  app/
  ├── api.py          - FastAPI app
  ├── gunicorn.py     - WSGI script
  └── schemas.py      - API model schemas
  ```
- Install the dependencies
  - FastAPI (`pip install "fastapi[all]"`)
    (this also installs `uvicorn`, which we'll be using as a server);
- Copy the basic snippets from the [MadeWithML tutorial](https://madewithml.com/courses/mlops/api/) and make sure that it all works.


