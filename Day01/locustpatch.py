from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def update_employee_email(self):

        payload = {
            "email": "john.smith@example.com"
        }

        with self.client.patch(
            "/patch",
            json=payload,
            name="Update Employee Email",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Expected 200, but received {response.status_code}"
                )
                
