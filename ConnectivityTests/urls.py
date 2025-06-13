from django.urls import path
from . import views

urlpatterns = [
    path('/', views.Employees.as_view(), name='GetEmployeesList'),
]