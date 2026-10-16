from locust import HttpUser, task, between


class EmployeeUser(HttpUser):
    wait_time = between(1, 3)

    @task(10)
    def get_employees(self):
        self.client.get(
            "/api/employees/",
            name="Get Employees",
        )

    @task(4)
    def view_page_1(self):
        self.client.get(
            "/api/employees/?page=1",
            name="Pagination - Page 1",
        )

    @task(3)
    def view_page_2(self):
        self.client.get(
            "/api/employees/?page=2",
            name="Pagination - Page 2",
        )

    @task(2)
    def invalid_page(self):
        with self.client.get(
            "/api/employees/?page=10000000",
            name="Get Employees - Invalid Page",
            catch_response=True,
        ) as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(
                    f"Expected 404, got {response.status_code}"
                )

    @task(1)
    def invalid_parameter(self):
        with self.client.get(
            "/api/employees/?page=invalid",
            name="Get Employees - Invalid Parameter",
            catch_response=True,
        ) as response:
            if response.status_code == 404:
                try:
                    data = response.json()
                    if data.get("detail") == "Invalid page.":
                        response.success()
                    else:
                        response.failure(
                            f"Unexpected response: {data}"
                        )
                except ValueError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(
                    f"Expected 404, got {response.status_code}"
                )


