import time
from locust import HttpUser, task, between


class TypicalIrisUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def sanity_check(self):
        self.client.get("/")

    @task(5)
    def logreg_prediction(self):
        flower_data = {
            "sepal_length": 6.4,
            "sepal_width": 2.8,
            "petal_length": 5.6,
            "petal_width": 2.1,
        }
        self.client.post("/models/LogisticRegression", json=flower_data)

    @task(5)
    def SVC_prediction(self):
        flower_data = {
            "sepal_length": 6.4,
            "sepal_width": 2.8,
            "petal_length": 5.6,
            "petal_width": 2.1,
        }
        self.client.post("/models/SVC", json=flower_data)
