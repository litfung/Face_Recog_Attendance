from django.contrib import admin
from .models import AttendanceRecord, PendingAlerts

# Register your models here.
admin.site.register(AttendanceRecord)
admin.site.register(PendingAlerts)