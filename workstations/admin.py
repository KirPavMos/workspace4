from django.contrib import admin
from .models import Workstation

@admin.register(Workstation)
class WorkstationAdmin(admin.ModelAdmin):
    list_display = ('desk_number', 'name', 'location', 'is_active', 'get_employee')
    list_filter = ('is_active', 'location')
    search_fields = ('desk_number', 'name', 'location')
    list_editable = ('is_active',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('desk_number', 'name', 'location', 'is_active')
        }),
        ('Описание', {
            'fields': ('description', 'equipment', 'notes'),
            'classes': ('collapse',)
        }),
        ('Техническая информация', {
            'fields': ('ip_address',),
            'classes': ('collapse',)
        }),
    )

    def get_employee(self, obj):
        if hasattr(obj, 'employee'):
            return obj.employee
        return "Не назначено"
    get_employee.short_description = 'Сотрудник'