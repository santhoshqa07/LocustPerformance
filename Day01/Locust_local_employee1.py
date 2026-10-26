

from locust import HttpUser, task, between


class ResponseValidationUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def validate_employee_response(self):
        with self.client.get(
            "/api/employees/",
            name="Validate Employee Response",
            catch_response=True,
        ) as response:

            # Check 1: HTTP status
            if response.status_code != 200:
                response.failure(
                    f"Expected 200, got {response.status_code}"
                )
                return

            # Check 2: Valid JSON
            try:
                data = response.json()
            except ValueError:
                response.failure("Response is not valid JSON")
                return

            # Check 3: Required response fields
            required_fields = {
                "count", "next", "previous", "results"
            }

            if not required_fields.issubset(data.keys()):
                response.failure("Missing required response fields")
                return

            # Check 4: Employee count
            if data["count"] != 10003:
                response.failure(
                    f"Expected count 10003, got {data['count']}"
                )
                return

            # Check 5: Results must be a list
            if not isinstance(data["results"], list):
                response.failure("'results' must be a list")
                return

            # Check 6: Validate employee fields
            required_employee_fields = {
                "id", "name", "email", "role",
                "department", "is_active"
            }

            for employee in data["results"]:
                if not required_employee_fields.issubset(employee.keys()):
                    response.failure("Employee record has missing fields")
                    return

            response.success()