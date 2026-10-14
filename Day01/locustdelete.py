from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def delete_employee(self):


        with self.client.delete(
            "/delete",

            name="Delete Employee",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Expected 200, but received {response.status_code}"
                )


