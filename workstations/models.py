from django.db import models


# Create your models here.
class Workstation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    location = models.CharField(max_length=100, verbose_name="Местоположение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["name"]

    def __str__(self):
        return self.name
