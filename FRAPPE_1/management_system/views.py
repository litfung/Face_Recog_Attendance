from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Employee, EmployeePhotos
from .forms import RegisterForm, LoginForm, EmployeeForm, PwdForm, DeleteEmpForm, ViewAttendanceForm, AdminAttendanceForm, AddEmployeeForm, AddEmployeePhotos
from django.contrib.auth.mixins import LoginRequiredMixin
from .functions import getLatestEmp, add_employee_api, delete_employee_api
from django.views.generic import View
from attendance_system.models import AttendanceRecord, PendingAlerts
from attendance_system.functions import day_diff, date_array
from datetime import datetime
from .charts import chart
from django.http import HttpResponse


def logout_view(request):
    logout(request)
    return redirect('management_system:login')


class LoginView(View):
    form_class = LoginForm
    template_name = 'management_system/login_form.html'

    def get(self, request):
        if request.user.username:
            return redirect('management_system:admin-detail')
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        try:
            form = self.form_class(request.POST)
            username = request.POST['username']
            employee = Employee.objects.get(pk=int(username))
            if request.POST['admin_login'] == '2':
                if employee.has_admin_acc:
                    password = request.POST['password']
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('management_system:admin-detail')
                    else:
                        error_message = 'Employee_ID or Password Is Incorrect'
                else:
                    error_message = 'You are not an admin'
            else:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('management_system:emp-detail')
                else:
                    error_message = 'Employee_ID or Password Is Incorrect'
        except:
            error_message = 'Employee Does not exist'

        return render(request, self.template_name, {'form': form, 'error_message': error_message})


# Employee
class EmployeeDetails(LoginRequiredMixin, generic.DetailView):
    model = Employee
    template_name = "management_system/Employee_HomePage.html"

    def get_object(self, queryset = None):
        pk = int(self.request.user.username)
        return Employee.objects.get(pk=pk)


class PwdChange(LoginRequiredMixin, View):
    form_class = PwdForm
    template_name = 'management_system/Employee_change_pwd.html'

    # display blank form
    def get(self,request):
        form = self.form_class(None)
        emp = Employee.objects.get(pk=int(request.user.username))
        return render(request, self.template_name, {'form': form, "employee":emp})

    # Process form data
    def post(self,request):
        form = self.form_class(request.POST)
        emp = Employee.objects.get(pk=int(request.user.username))
        username = request.user.username
        password = request.POST['old_password']
        n_password = request.POST['new_password']
        c_password = request.POST['r_new_password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if n_password == c_password:
                new_password = n_password
                user.set_password(new_password)
                user.save()
                user1 = authenticate(username=username, password=new_password)
                if user1 is not None:
                    login(request, user1)
                    return redirect('management_system:emp-detail')
            else:
                return render(request, self.template_name, {'form': form, 'error_message': 'The new password does not match the password required for confirmation. Please Try Again', "employee":emp})
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Incorrect. Please Try Again', "employee":emps})

        return redirect('management_system:emp-detail')


class UpdateDetails(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'management_system/Employee_update_form.html'
    success_url = reverse_lazy('management_system:update')

    def get_object(self, queryset=None):
        pk = int(self.request.user.username)
        return Employee.objects.get(pk=pk)


class ViewAttendanceRecords(LoginRequiredMixin, View):
    model = AttendanceRecord
    template_name = 'management_system/employee-attendance.html'
    form_class = ViewAttendanceForm

    def get(self, request):
        form = self.form_class(None)
        duration = 'for the current month'
        now = datetime.now()
        string = now.strftime('%m-%Y')
        initial_date = '01-'+string
        final_date = now.strftime('%d-%m-%Y')
        total_days = day_diff(initial_date, final_date)
        emp = Employee.objects.get(pk = int(request.user.username))
        records = emp.attendancerecord_set.filter(date__endswith=string)
        present = records.count()
        pie3d = chart(request, total_days, present)
        return render(request, self.template_name, {'form':form, 'records':records, 'duration':duration, 'output':pie3d.render(), 'employee':emp})

    def post(self, request):
        form = self.form_class(request.POST)
        initial_date = request.POST['startdate'] + "-" + request.POST['startmonth'] + "-" + request.POST['startyear']
        final_date = request.POST['enddate'] + "-" + request.POST['endmonth'] + "-" + request.POST['endyear']
        duration = 'from ' + initial_date + ' to ' + final_date
        datearray = date_array(initial_date, final_date)
        total_days = day_diff(initial_date, final_date)
        emp = Employee.objects.get(pk = int(request.user.username))
        records = []
        for date in datearray:
            for i in emp.attendancerecord_set.filter(date=date):
                records.append(i)
        present = len(records)
        pie3d = chart(request, total_days, present)
        return render(request, self.template_name, {'form': form, 'records': records, 'duration': duration, 'output': pie3d.render(),'employee':emp})


# Administrator
class AdminDetails(LoginRequiredMixin, View):
    model = Employee
    template_name = "management_system/Admin_HomePage.html"

    def get(self, request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            return render(request, self.template_name, {'employee': employee})
        else:
            return redirect('management_system:emp-detail')


# class AddEmployee(LoginRequiredMixin, CreateView):
#     model = Employee
#     fields = ['phone', 'email', 'first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'profile_pic']
#     template_name = 'management_system/Admin_add_employee.html'
#     success_url = reverse_lazy('management_system:a-update')


class AddEmployee(LoginRequiredMixin, View):
    form_class1 = AddEmployeeForm
    form_class2 = AddEmployeePhotos
    template_name = 'management_system/Admin_add_employee.html'

    def get(self,request):
        form1 = self.form_class1(None)
        form2 = self.form_class2(None)
        user = Employee.objects.get(pk=int(request.user.username))
        if user.has_admin_acc:
            return render(request, self.template_name, {"form1":form1, "form2":form2})
        else:
            return redirect('management-system:update')

    def post(self,request):
        form1 = self.form_class1(request.POST, request.FILES)
        form2 = self.form_class2(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            employee = Employee()
            employee.email = form1.cleaned_data.get('email')
            employee.phone = form1.cleaned_data.get('phone')
            employee.first_name = form1.cleaned_data.get('first_name')
            employee.last_name = form1.cleaned_data.get('last_name')
            employee.address = form1.cleaned_data.get('address')
            employee.city = form1.cleaned_data.get('city')
            employee.country = form1.cleaned_data.get('country')
            employee.zip_code = form1.cleaned_data.get('zip_code')
            employee.profile_pic = form1.cleaned_data.get('profile_pic')
            employee.save()
            photos = EmployeePhotos()
            photos.employee = employee
            photos.pic0 = form2.cleaned_data.get('pic0')
            photos.pic1 = form2.cleaned_data.get('pic1')
            photos.pic2 = form2.cleaned_data.get('pic2')
            photos.pic3 = form2.cleaned_data.get('pic3')
            photos.pic4 = form2.cleaned_data.get('pic4')
            photos.save()
            paths = [photos.pic0.path,photos.pic1.path,photos.pic2.path,photos.pic3.path,photos.pic4.path]
            code = add_employee_api(employee.emp_id, paths)
            if code == 'success':
                return redirect('management_system:a-update')
            else:
                employee.delete()
        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'error_message': 'Could not add employee. Try Again Later!'})


class DeleteEmployee(LoginRequiredMixin, View):
    form_class = DeleteEmpForm
    model = Employee

    def get(self, request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            form = self.form_class(None)
            return render(request, 'management_system/Admin_delete_employee.html', {'form':form})
        else:
            return redirect('management_system:emp-detail')

    def post(self, request):
        form = self.form_class(request.POST)
        emp_id = request.POST['emp_id']
        r_emp_id = request.POST['r_emp_id']
        if emp_id != r_emp_id:
            return render(request, 'management_system/Admin_delete_employee.html', {'form': form, 'error_message':'The employee IDs dont match'})
        else:
            try:
                code = delete_employee_api(emp_id)
                if code == "success":
                    instance = Employee.objects.get(pk=emp_id)
                    instance.delete()
                    return redirect('management_system:remove-employee')
                else:
                    return render(request, 'management_system/Admin_delete_employee.html', {'form': form, 'error_message': 'The employee IDs dont match'})
            except:
                return render(request, 'management_system/Admin_delete_employee.html', {'form': form, 'error_message': 'The employee does not exist'})


class APwdChange(LoginRequiredMixin, View):
    form_class = PwdForm
    template_name = 'management_system/Admin_change_pwd.html'

    # display blank form
    def get(self,request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form})
        else:
            return redirect('management_system:change-password')

    # Process form data
    def post(self,request):
        form = self.form_class(request.POST)
        username = request.user.username
        password = request.POST['old_password']
        n_password = request.POST['new_password']
        c_password = request.POST['r_new_password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if n_password == c_password:
                new_password = n_password
                user.set_password(new_password)
                user.save()
                user1 = authenticate(username=username, password=new_password)
                if user1 is not None:
                    login(request, user1)
                    return redirect('management_system:admin-detail')
            else:
                return render(request, self.template_name, {'form': form, 'error_message': 'The new password does not match the password required for confirmation. Please Try Again'})
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Incorrect. Please Try Again'})

        return redirect('management_system:admin-detail')


class RegisterView(LoginRequiredMixin, View):
    form_class = RegisterForm
    template_name = 'management_system/registration_form.html'

    def get(self, request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            form = self.form_class(None)
            form.fields['username'].initial = getLatestEmp()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('management_system:change-password')

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalised) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect("management_system:add-employee")

        return render(request, self.template_name, {'form': form})


class AUpdateDetails(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'management_system/Admin_update_form.html'
    success_url = reverse_lazy('management_system:register-user')

    def get_object(self, queryset=None):
        key = Employee.objects.all()[Employee.objects.all().count()-1].pk
        return Employee.objects.get(pk=key)


class AViewAttendanceRecords(LoginRequiredMixin, View):
    model = AttendanceRecord
    template_name = 'management_system/admin-attendance.html'
    form_class = AdminAttendanceForm

    def get(self, request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            form = self.form_class(None)
            duration = 'for the current month'
            now = datetime.now()
            string = now.strftime('%m-%Y')
            records = AttendanceRecord.objects.filter(date__endswith=string)
            return render(request, self.template_name, {'form':form, 'records':records, 'duration':duration})
        else:
            return redirect("management_system:check-attendance")

    def post(self, request):
        form = self.form_class(request.POST)
        error_message = ''
        duration = "for the current month"
        try:
            if request.POST['emp_id'] and request.POST['startdate'] and request.POST['startmonth'] and request.POST['startyear'] and request.POST['enddate'] and request.POST['endmonth'] and request.POST['endyear']:
                emp = Employee.objects.get(pk=int(request.POST['emp_id']))
                initial_date = request.POST['startdate'] + "-" + request.POST['startmonth'] + "-" + request.POST['startyear']
                final_date = request.POST['enddate'] + "-" + request.POST['endmonth'] + "-" + request.POST['endyear']
                duration = 'for Employee ID: '+ request.POST["emp_id"] + ' from ' + initial_date + ' to ' + final_date
                datearray = date_array(initial_date, final_date)
                total_days = day_diff(initial_date, final_date)
                records = []
                for date in datearray:
                    for i in emp.attendancerecord_set.filter(date=date):
                        records.append(i)
                present = len(records)
                pie3d = chart(request, total_days, present)
                return render(request, self.template_name,{'form': form, 'records': records, 'duration': duration,'output':pie3d.render()})
            elif request.POST['emp_id']:
                emp = Employee.objects.get(pk=int(request.POST['emp_id']))
                duration = 'for Employee ID: ' + request.POST["emp_id"] + ' for the current month'
                now = datetime.now()
                string = now.strftime('%m-%Y')
                initial_date = '01-' + string
                final_date = now.strftime('%d-%m-%Y')
                total_days = day_diff(initial_date, final_date)
                records = emp.attendancerecord_set.filter(date__endswith=string)
                present = records.count()
                pie3d = chart(request, total_days, present)
                return render(request, self.template_name,{'form': form, 'records': records, 'duration': duration, 'output': pie3d.render()})
            elif request.POST['startdate'] and request.POST['startmonth'] and request.POST['startyear'] and request.POST['enddate'] and request.POST['endmonth'] and request.POST['endyear']:
                initial_date = request.POST['startdate'] + "-" + request.POST['startmonth'] + "-" + request.POST['startyear']
                final_date = request.POST['enddate'] + "-" + request.POST['endmonth'] + "-" + request.POST['endyear']
                duration = 'from ' + initial_date + ' to ' + final_date
                datearray = date_array(initial_date, final_date)
                records = []
                for date in datearray:
                    for i in AttendanceRecord.objects.filter(date=date):
                        records.append(i)
                return render(request, self.template_name,{'form': form, 'records': records, 'duration': duration})
            else:
                form = self.form_class(None)
                duration = 'for the current month'
                now = datetime.now()
                string = now.strftime('%m-%Y')
                records = AttendanceRecord.objects.filter(date__endswith=string)
                return render(request, self.template_name, {'form': form, 'records': records, 'duration': duration})
        except:
            now = datetime.now()
            string = now.strftime('%m-%Y')
            records = AttendanceRecord.objects.filter(date__endswith=string)
            error_message = "Employee does not Exist"
            return render(request, self.template_name, {'form': form, 'records': records, 'duration': duration, "error_message":error_message})


class AAlerts(LoginRequiredMixin, View):
    model = PendingAlerts
    template_name = 'management_system/admin-request.html'
    trial_name = 'management_system/admin-trial.html'

    def get(self,request):
        employee = Employee.objects.get(pk=int(request.user.username))
        if employee.has_admin_acc:
            alerts = PendingAlerts.objects.all()
            return render(request, self.template_name, {"alerts":alerts})
        else:
            return redirect("management_system:alerts")

    def post(self, request):
        alerts = PendingAlerts.objects.all()
        index = -1
        operation = str()
        for i in range(len(alerts)):
            access_string = 'acc'+str(i)
            delete_string = 'del'+str(i)
            if request.POST.get(access_string):
                index = i
                operation = 'save'
            elif request.POST.get(delete_string):
                index = i
                operation = 'delete'

        alert = alerts[index]
        if operation == 'save':
            record = AttendanceRecord()
            record.emp = alert.emp
            record.date = alert.date
            record.time = alert.time
            record.was_alert = True
            record.save()
            alert.delete()
        elif operation == 'delete':
            alert.delete()
        alerts = PendingAlerts.objects.all()
        return render(request, self.template_name, {'alerts':alerts})


