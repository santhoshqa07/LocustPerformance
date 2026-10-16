
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

    @task
    def get_invalid_employee_page(self):
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



    @task
    def validate_pagination(self):
        # Check page 1
        with self.client.get(
                "/api/employees/?page=1",
                name="Pagination - Page 1",
                catch_response=True,
        ) as response1:
            if response1.status_code != 200:
                response1.failure(
                    f"Page 1 returned {response1.status_code}"
                )
                return

            try:
                data1 = response1.json()
                ids1 = {item["id"] for item in data1["results"]}

                if len(ids1) != 100:
                    response1.failure("Page 1 should contain 100 records")
                    return

                if not isinstance(data1.get("results"), list):
                    response1.failure("Missing or invalid results list")
                elif data1.get("count") != 10003:
                    response1.failure("Unexpected total employee count")
                elif len(data1["results"]) != 100:
                    response1.failure("Page 1 should contain 100 records")

            except (ValueError, KeyError, TypeError):
                response1.failure("Invalid page 1 response structure")
                return

        # Check page 2
        with self.client.get(
                "/api/employees/?page=2",
                name="Pagination - Page 2",
                catch_response=True,
        ) as response2:
            if response2.status_code != 200:
                response2.failure(
                    f"Page 2 returned {response2.status_code}"
                )
                return

            try:
                data2 = response2.json()
                ids2 = {item["id"] for item in data2["results"]}

                if len(ids2) != 100:
                    response2.failure("Page 2 should contain 100 records")
                elif ids1.intersection(ids2):
                    response2.failure("Duplicate IDs across pages")

                if not isinstance(data2.get("results"), list):
                    response2.failure("Missing or invalid results list")
                elif len(data2["results"]) != 100:
                    response2.failure("Page 2 should contain 100 records")
                elif ids1.intersection(
                        item["id"] for item in data2["results"]
                ):
                    response2.failure("Duplicate IDs across pages")


            except (ValueError, KeyError, TypeError):
                response2.failure("Invalid page 2 response structure")

    @task
    def get_employees_with_invalid_parameter(self):
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
                            f"Unexpected error message: {data}"
                        )

                except (ValueError, AttributeError):
                    response.failure("Invalid JSON error response")

            else:
                response.failure(
                    f"Expected 404, got {response.status_code}"
                )
