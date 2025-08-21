from django.db import models

class Workstation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    desk_number = models.CharField(max_length=20, verbose_name="Номер стола", unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    location = models.CharField(max_length=100, verbose_name="Местоположение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    # Дополнительные поля по желанию
    equipment = models.TextField(blank=True, verbose_name="Оборудование")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP-адрес")
    notes = models.TextField(blank=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["desk_number"]

    def __str__(self):
        return f"{self.desk_number} - {self.name}"