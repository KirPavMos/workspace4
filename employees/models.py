from django.db import models

from workstations.models import Workstation


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    position = models.CharField(max_length=100, verbose_name="Должность")
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рабочее место",
    )
    hire_date = models.DateField(verbose_name="Дата приема на работу")
    email = models.EmailField(unique=True, verbose_name="Email")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
