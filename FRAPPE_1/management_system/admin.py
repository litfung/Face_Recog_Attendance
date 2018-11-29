from django.contrib import admin
from .models import Employee, EmployeePhotos

# Register your models here.
admin.site.register(Employee)
admin.site.register(EmployeePhotos)