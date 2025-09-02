from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Employee, EmployeeImage, EmployeeSkill, Skill

class HomeView(ListView):
    model = Employee
    template_name = 'employees/home.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        # Получаем 4 последних сотрудника по дате приёма
        return Employee.objects.prefetch_related(
            Prefetch('images', queryset=EmployeeImage.objects.order_by('order')),
            Prefetch('employeeskill_set', queryset=EmployeeSkill.objects.select_related('skill'))
        ).order_by('-hire_date')[:4]  # 4 последних по дате приёма
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем общее количество сотрудников
        context['total_employees'] = Employee.objects.count()
        return context

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            Prefetch('images', queryset=EmployeeImage.objects.order_by('order')),
            Prefetch('employeeskill_set', queryset=EmployeeSkill.objects.select_related('skill'))
        ).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Не нужно добавлять work_experience_days в объекты, так как это свойство
        # Оно уже доступно через employee.work_experience_days в шаблоне
        return context

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            Prefetch('images', queryset=EmployeeImage.objects.order_by('order')),
            Prefetch('employeeskill_set', queryset=EmployeeSkill.objects.select_related('skill'))
        ).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = context['employee']
        
        # Получаем все изображения сотрудника
        all_images = employee.images.all()
        
        # Первое изображение - заглавное фото
        first_image = all_images.first() if all_images.exists() else None
        
        # Остальные изображения для галереи (без первого)
        gallery_images = all_images[1:] if all_images.count() > 1 else []
        
        # Добавляем в контекст
        context['first_image'] = first_image
        context['gallery_images'] = gallery_images
        # work_experience_days доступен через свойство employee.work_experience_days
        
        return context
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view, login_url='/admin/login/')