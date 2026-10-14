from locust import HttpUser, task, between



class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def create_employee(self):

        payload = {
            "name": "John",
            "email": "john@example.com",
            "role": "employee"
        }

        with self.client.post(
            "/post",
            json=payload,
            name="Create Employee",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                f"Expected 200, but received {response.status_code}"
            )