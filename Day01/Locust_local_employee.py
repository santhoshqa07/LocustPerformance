
from locust import HttpUser, task, between


class EmployeeUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def get_employees(self):
        with self.client.get(
            "/api/employees/",
            name="Get Employees",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Expected 200, but received {response.status_code}"
                )



                
