from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Employee

#
# @api_view(["GET"])
# def employee_list(request):
#     employees = Employee.objects.all()
#
#     data = [
#         {
#             "id": employee.id,
#             "name": employee.name,
#             "email": employee.email,
#             "role": employee.role,
#             "department": employee.department,
#             "is_active": employee.is_active,
#         }
#         for employee in employees
#     ]
#
#     return Response(data)
#     return paginator.get_paginated_response(data)


from django.shortcuts import render

# Create your views here.


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Employee


@api_view(["GET"])
def employee_list(request):
    # Step 1: Create the paginator
    paginator = PageNumberPagination()
    paginator.page_size = 100

    # Step 2: Get employees in a consistent order
    employees = Employee.objects.all().order_by("id")

    # Step 3: Retrieve only the requested page
    page = paginator.paginate_queryset(employees, request)

    # Step 4: Convert the page's employees into dictionaries
    data = [
        {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role,
            "department": employee.department,
            "is_active": employee.is_active,
        }
        for employee in page
    ]

    # Step 5: Return the paginated response
    return paginator.get_paginated_response(data)

