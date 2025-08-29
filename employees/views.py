from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Employee

class HomeView(ListView):
    model = Employee
    template_name = 'employees/home.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            'employeeskill_set__skill', 
            'images'
        ).all()[:6]  # Показываем только 6 сотрудников на главной

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 12
    
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            'employeeskill_set__skill', 
            'images'
        ).all()

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            'employeeskill_set__skill', 
            'images'
        ).all()
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view, login_url='/admin/login/')