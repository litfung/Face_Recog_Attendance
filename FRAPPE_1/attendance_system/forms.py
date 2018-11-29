from django import forms
from .models import AttendanceRecord, PendingAlerts
from management_system.models import Employee


class AttendanceRecordForm(forms.ModelForm):
    emp_id = forms.IntegerField()

    class Meta:
        model = AttendanceRecord
        fields = ['emp_id']

