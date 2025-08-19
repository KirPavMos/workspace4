from django.contrib import admin

from .models import Workstation


@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_active")
    list_filter = ("is_active", "location")
    search_fields = ("name", "description")
