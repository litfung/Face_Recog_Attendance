from django.db import models
from management_system.models import Employee


# Create your models here.
class AttendanceRecord(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    was_alert = models.BooleanField(default=False)

    def __str__(self):
        string = str(self.emp.emp_id) + ' -- ' + self.date + ' -- ' + self.time
        return string


class PendingAlerts(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

    def __str__(self):
        string = str(self.emp.emp_id) + ' -- ' + self.date + ' -- ' + self.time
        return string

