from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
from django.utils.translation import gettext_lazy as _

from django.apps import apps

def validate_no_adjacent_tables(value, employee_instance=None):
    # Используем строковые ссылки на модели
    Workstation = apps.get_model('workstations', 'Workstation')
    Employee = apps.get_model('employees', 'Employee')
    
    if not value:  # Если workstation не установлен
        return
    
    # Получаем номер стола из workstation
    table_number = None
    
    if isinstance(value, int):
        try:
            workstation = Workstation.objects.get(id=value)
            table_number = workstation.table_number
        except Workstation.DoesNotExist:
            return
    else:
        # Если value - это объект Workstation
        table_number = value.table_number
    
    # Проверяем, что номер стола существует и является числом
    if not table_number:
        return
    
    # Преобразуем table_number в число (если оно хранится как строка)
    try:
        table_number_int = int(table_number)
    except (ValueError, TypeError):
        return  # Если номер стола не является числом, пропускаем проверку
    
    # Получаем текущего сотрудника
    if not hasattr(validate_no_adjacent_tables, '_current_instance'):
        return
    
    current_employee = validate_no_adjacent_tables._current_instance
    
    # Получаем всех сотрудников за соседними столами
    adjacent_tables = [table_number_int - 1, table_number_int + 1]
    
    # Находим рабочие места с соседними столами
    adjacent_workstations = Workstation.objects.filter(
        table_number__in=[str(t) for t in adjacent_tables]
    )
    
    # Получаем сотрудников на соседних рабочих местах
    adjacent_employees = Employee.objects.filter(workstation__in=adjacent_workstations)
    
    # Проверяем, есть ли среди соседей тестировщики или разработчики
    for emp in adjacent_employees:
        if emp == current_employee or not emp.workstation:  # Пропускаем текущего сотрудника и без рабочего места
            continue
        
        # Получаем номер стола соседнего сотрудника
        emp_table_number = emp.workstation.table_number
        
        is_tester = 'тестировщик' in emp.position.lower() or 'tester' in emp.position.lower()
        is_developer = any(word in emp.position.lower() for word in ['разработчик', 'developer', 'backend', 'frontend'])
        
        current_is_tester = 'тестировщик' in current_employee.position.lower() or 'tester' in current_employee.position.lower()
        current_is_developer = any(word in current_employee.position.lower() for word in ['разработчик', 'developer', 'backend', 'frontend'])
        
        if (is_tester and current_is_developer) or (is_developer and current_is_tester):
            raise ValidationError(
                f'Тестировщики и разработчики не могут сидеть за соседними столами. '
                f'Стол {table_number} соседствует со столом {emp_table_number} '
                f'(сотрудник: {emp.first_name} {emp.last_name}, должность: {emp.position})'
            )

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    email = models.EmailField(verbose_name='Email', unique=True)
    position = models.CharField(max_length=200, verbose_name='Должность')
    hire_date = models.DateField(verbose_name='Дата приема на работу', default=timezone.now)
    workstation = models.ForeignKey(
        'workstations.Workstation', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Рабочее место'
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    def clean(self):
        """Валидация при сохранении"""
        super().clean()
        
        # Сохраняем текущий экземпляр для использования в валидаторе
        validate_no_adjacent_tables._current_instance = self
        
        # Валидируем workstation
        if self.workstation:
            validate_no_adjacent_tables(self.workstation)
    
    def save(self, *args, **kwargs):
        """Переопределяем save для обязательной валидации"""
        # Валидируем перед сохранением
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Очищаем временную переменную
        if hasattr(validate_no_adjacent_tables, '_current_instance'):
            delattr(validate_no_adjacent_tables, '_current_instance')
    
    @property
    def work_experience_days(self):
        """Стаж работы в днях"""
        if self.hire_date:
            return (timezone.now().date() - self.hire_date).days
        return 0
    
    @property
    def table_number(self):
        """Номер стола сотрудника"""
        if self.workstation:
            return self.workstation.table_number
        return None

# Остальные модели
class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name='Навык')
    description = models.TextField(verbose_name='Описание навыка', blank=True)
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
    
    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    LEVEL_CHOICES = [
        (1, 'Начальный'),
        (2, 'Средний'),
        (3, 'Продвинутый'),
        (4, 'Эксперт'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='Навык')
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Уровень')
    
    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'
        unique_together = ['employee', 'skill']
    
    def __str__(self):
        return f'{self.employee} - {self.skill} ({self.get_level_display()})'


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='Сотрудник'
    )
    image = models.ImageField(
        upload_to='employees/%Y/%m/%d/',
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядковый номер'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Изображение сотрудника'
        verbose_name_plural = 'Изображения сотрудников'
        ordering = ['employee', 'order', 'created_at']
    
    def __str__(self):
        return f'Изображение {self.order} для {self.employee}'
    
    def delete(self, *args, **kwargs):
        # Удаляем файл изображения при удалении объекта
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def clean(self):
        # Валидация порядка
        if self.order < 0:
            raise ValidationError({'order': 'Порядковый номер не может быть отрицательным'})