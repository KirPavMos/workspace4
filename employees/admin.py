from django.contrib import admin
from .models import Employee, Skill, EmployeeSkill, EmployeeImage


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
    fields = ["image", "order", "created_at"]
    readonly_fields = ["created_at"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "workstation", "email")
    list_filter = ("position", "gender")
    search_fields = ("last_name", "first_name", "email")
    inlines = [
        EmployeeSkillInline,
        EmployeeImageInline,
    ]  # Добавляем галерею изображений
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("last_name", "first_name", "middle_name", "gender")},
        ),
        ("Контактная информация", {"fields": ("email",)}),
        (
            "Профессиональная информация",
            {"fields": ("position", "hire_date", "workstation")},
        ),
        ("Дополнительно", {"fields": ("description",), "classes": ("collapse",)}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ("employee", "skill", "level")
    list_filter = ("skill", "level")


@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = ("employee", "order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("employee__first_name", "employee__last_name")
    ordering = ["employee", "order"]
