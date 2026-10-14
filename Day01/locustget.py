from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def get_user_details(self):

        with self.client.get(
            "/get",
            params={"user": "employee01", "role": "employee"},
            name="Get User Details",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Expected 200, but received {response.status_code}"
                )


