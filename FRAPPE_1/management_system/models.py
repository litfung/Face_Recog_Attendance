from django.db import models


# Create your models here.
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    profile_pic = models.FileField(upload_to='media', default='profile-photo.jpg')
    has_admin_acc = models.BooleanField(default=False)

    def __str__(self):
        string = str(self.emp_id) + " -- " + self.first_name + " " + self.last_name
        return string


class EmployeePhotos(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    pic0 = models.FileField(upload_to='media')
    pic1 = models.FileField(upload_to='media')
    pic2 = models.FileField(upload_to='media')
    pic3 = models.FileField(upload_to='media')
    pic4 = models.FileField(upload_to='media')

    def __str__(self):
        string = str(self.employee.emp_id)
        return string



class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        string = str(self.employee.emp_id)
        return string