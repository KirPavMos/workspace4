from django.contrib import admin
from .models import Employee, Skill, EmployeeSkill

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'workstation', 'email')
    list_filter = ('position', 'gender')
    search_fields = ('last_name', 'first_name', 'email')
    inlines = [EmployeeSkillInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'middle_name', 'gender')
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

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'skill', 'level')
    list_filter = ('skill', 'level')