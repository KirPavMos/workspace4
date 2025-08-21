from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Модель для навыков
class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")
    description = models.TextField(blank=True, verbose_name="Описание навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name

# Модель для связи сотрудника с навыком и уровнем владения
class EmployeeSkill(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Сотрудник")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.PositiveSmallIntegerField(
        verbose_name="Уровень владения",
        choices=[(i, f"{i}") for i in range(1, 11)],
        default=1
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        unique_together = ('employee', 'skill')

    def __str__(self):
        return f"{self.employee} - {self.skill} (уровень: {self.level})"

# Основная модель сотрудника
class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),        
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="employee_profile",
        null=True,
        blank=True
    )
    
    # Основная информация
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Пол",
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        blank=True,
        null=True
    )
    
    # Контактная информация
    email = models.EmailField(unique=True, verbose_name="Email", blank=True, null=True)
    
    # Профессиональная информация
    position = models.CharField(max_length=100, verbose_name="Должность", blank=True, null=True)
    hire_date = models.DateField(verbose_name="Дата приема на работу", default=timezone.now)
    
    # Описание (можно позже добавить WYSIWYG-редактор)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    
    # Связи
    skills = models.ManyToManyField(
        Skill,
        through=EmployeeSkill,
        verbose_name="Навыки",
        related_name="employees",
        blank=True
    )
    workstation = models.ForeignKey(
        'workstations.Workstation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рабочее место"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

# Сигналы для автоматического создания профиля сотрудника при создании пользователя
@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        # Создаем профиль сотрудника с базовой информацией
        Employee.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            position="Не указана",
            hire_date=timezone.now().date()
        )

@receiver(post_save, sender=User)
def save_employee_profile(sender, instance, **kwargs):
    if hasattr(instance, 'employee_profile'):
        instance.employee_profile.save()