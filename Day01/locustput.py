
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def update_employee(self):

        payload = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "role": "employee"
        }

        with self.client.put(
            "/put",
            json=payload,
            name="Update Employee",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Expected 200, but received {response.status_code}"
                )

