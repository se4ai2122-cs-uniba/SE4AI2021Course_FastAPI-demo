import random
from locust import HttpUser, task, between


class TypicalIrisUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def sanity_check(self):
        self.client.get("/")

    @task(5)
    def logreg_prediction(self):
        flower_data = {
            "sepal_length": random.uniform(4.3, 7.9),
            "sepal_width": random.uniform(2.0, 4.4),
            "petal_length": random.uniform(1.0, 6.9),
            "petal_width": random.uniform(0.1, 2.5),
        }
        self.client.post("/models/LogisticRegression", json=flower_data)

    @task(5)
    def SVC_prediction(self):
        flower_data = {
            "sepal_length": random.uniform(4.3, 7.9),
            "sepal_width": random.uniform(2.0, 4.4),
            "petal_length": random.uniform(1.0, 6.9),
            "petal_width": random.uniform(0.1, 2.5),
        }
        self.client.post("/models/SVC", json=flower_data)
