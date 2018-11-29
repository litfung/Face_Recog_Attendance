from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .forms import AttendanceRecordForm
from .models import AttendanceRecord, PendingAlerts
from management_system.models import Employee, AttendanceLog
from django.views.generic.edit import CreateView
from .functions import current_date, current_time, face_recognise, getLatestLog
import base64


# Create your views here.
class RecogniseEmployee(View):
    template_name = 'attendance_system/main_page.html'

    def get(self,request):
        return render(request, self.template_name)

    def post(self,request):
        pic = AttendanceLog()
        imgdata = request.POST['inp_img']
        imgdata = imgdata[22:]
        image_data = str.encode(imgdata)
        with open("imageToSave.png", "wb") as f:
            f.write(base64.decodestring(image_data))
        emp_id = face_recognise("imageToSave.png")
        try:
            pic.employee = Employee.objects.get(pk=emp_id)
            pic.save()
            return redirect('attendance_system:mark-attendance')
        except:
            return redirect('attendance_system:raise_alert')



class MarkAttendance(View):
    form_class = AttendanceRecordForm
    template_name = 'attendance_system/attendance_form.html'

    def get(self, request):
        form = self.form_class(None)
        log_id = AttendanceLog.objects.latest('id')
        form.fields['emp_id'].initial = log_id.employee.emp_id
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        error_message = ''
        try:
            if form.is_valid():
                emp_id = form.cleaned_data['emp_id']
                emp = Employee.objects.get(pk=emp_id)
                record = AttendanceRecord()
                record.emp = emp
                record.date = current_date()
                record.time = current_time()
                record.save()
            else:
                error_message = "The Form is Invalid...."
            return redirect('attendance_system:rec-emp')
        except:
            error_message = "Invalid Employee ID...."
            return render(request, self.template_name, {'form': self.form_class(None), 'error_message':error_message})


class RaiseAlert(View):
    form_class = AttendanceRecordForm
    template_name = 'attendance_system/raise_alert.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'error_message': 'Error Recognising Face.'})

    def post(self,request):
        form = self.form_class(request.POST)
        error_message = ''
        try:
            if form.is_valid():
                emp_id = form.cleaned_data['emp_id']
                emp = Employee.objects.get(pk=emp_id)
                record = PendingAlerts()
                record.emp = emp
                record.date = current_date()
                record.time = current_time()
                record.save()
                return redirect('attendance_system:rec-emp')
            else:
                error_message = "The Form is Invalid...."
        except:
            error_message = "Invalid Employee ID...."
        return render(request, self.template_name, {'form': self.form_class(None), 'error_message':error_message})
