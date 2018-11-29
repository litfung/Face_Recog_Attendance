from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Employee, EmployeePhotos
from attendance_system.models import AttendanceRecord, PendingAlerts


class RegisterForm(UserCreationForm):
    username = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    admin_login = forms.ChoiceField(widget = forms.RadioSelect, choices=(('1','Employee'), ('2','Administrator')))

    class Meta:
        model = User
        fields = ['username', 'password', 'admin_login']


class EmployeeForm(forms.ModelForm):
    email = forms.EmailField()
    phone = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
    zip_code = forms.IntegerField()
    profile_pic = forms.FileField

    class Meta:
        model = Employee
        fields = ['phone', 'email', 'first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'profile_pic']


class PwdForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    r_new_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['old_password', 'r_new_password', 'r_new_password']


class DeleteEmpForm(forms.Form):
    emp_id = forms.IntegerField()
    r_emp_id = forms.IntegerField()

    class Meta:
        fields = ['emp_id', 'r_emp_id']


class ViewAttendanceForm(forms.Form):
    startdate = forms.IntegerField(min_value=1, max_value=31)
    startmonth = forms.IntegerField(min_value=1, max_value=12)
    startyear = forms.IntegerField(min_value=2018)
    enddate = forms.IntegerField(min_value=1, max_value=31)
    endmonth = forms.IntegerField(min_value=1, max_value=12)
    endyear = forms.IntegerField(min_value=2018)

    class Meta:
        fields = ['startdate', 'startmonth', 'startyear', 'enddate', 'endmonth', 'endyear']


class AdminAttendanceForm(forms.Form):
    emp_id = forms.IntegerField(required=False)
    startdate = forms.IntegerField(min_value=1, max_value=31,required=False)
    startmonth = forms.IntegerField(min_value=1, max_value=12,required=False)
    startyear = forms.IntegerField(min_value=2018,required=False)
    enddate = forms.IntegerField(min_value=1, max_value=31,required=False)
    endmonth = forms.IntegerField(min_value=1, max_value=12,required=False)
    endyear = forms.IntegerField(min_value=2018,required=False)

    class Meta:
        fields = ['emp_id','startdate', 'startmonth', 'startyear', 'enddate', 'endmonth', 'endyear']


class AddEmployeeForm(forms.ModelForm):
    email = forms.EmailField()
    phone = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
    zip_code = forms.IntegerField()
    profile_pic = forms.FileField()

    class Meta:
        model = Employee
        fields = ['phone', 'email', 'first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'profile_pic']


class AddEmployeePhotos(forms.ModelForm):

    class Meta:
        model = EmployeePhotos
        fields = ['pic0', 'pic1', 'pic2', 'pic3', 'pic4']