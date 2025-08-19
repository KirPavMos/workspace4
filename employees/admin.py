from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "workstation")
    list_filter = ("position", "workstation")
    search_fields = ("last_name", "first_name", "email")
    raw_id_fields = ("workstation",)
