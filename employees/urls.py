from django.urls import path
from .views import HomeView, EmployeeListView, EmployeeDetailView

app_name = "employees"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("employees/", EmployeeListView.as_view(), name="employee_list"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
]
