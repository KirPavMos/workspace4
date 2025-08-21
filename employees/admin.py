from django.contrib import admin
from .models import Skill, EmployeeSkill, Employee

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'skill', 'level')
    list_filter = ('skill', 'level')
    search_fields = ('employee__last_name', 'employee__first_name', 'skill__name')

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'position', 'gender', 'hire_date')
    list_filter = ('position', 'gender', 'hire_date')
    search_fields = ('last_name', 'first_name', 'middle_name', 'position', 'email')
    inlines = [EmployeeSkillInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'last_name', 'first_name', 'middle_name', 'gender')
        }),
        ('Контактная информация', {
            'fields': ('email',)
        }),
        ('Профессиональная информация', {
            'fields': ('position', 'hire_date', 'workstation')
        }),
        ('Дополнительно', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )