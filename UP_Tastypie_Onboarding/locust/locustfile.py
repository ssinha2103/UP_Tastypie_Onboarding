from locust import HttpUser, task, between
import base64


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    token = ""
    username = ""

    def on_start(self):
        """On starting the locust application user/login endpoint is hit and the user login gets checked"""
        payload = {"username": "mcd", "password": "mcd12345"}
        response = self.client.post("user/login/", json=payload)
        # response = response.json()
        # print(response)

    @task
    def view_stores(self):
        """Store endpoint is hit using this function"""
        response = self.client.get("stores/", auth=("mcd", "mcd12345"))

    @task
    def view_items(self):
        """Items endpoint is hit using this function"""
        response = self.client.get("items/", auth=("mcd", "mcd12345"))

    @task
    def see_orders(self):
        """Orders endpoint is hit using this function"""
        response = self.client.get("see_order/", auth=("mcd", "mcd12345"))
