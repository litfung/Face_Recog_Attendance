from .models import Employee
from attendance_system.face_functions import *


def getLatestEmp():
    key = Employee.objects.all()[Employee.objects.all().count()-1].pk
    return str(key)


def add_employee_api(emp_id, paths):
    person_id = create_person(emp_id)
    if person_id != 'Try Again Later':
        code = add_faces(person_id, paths)
        if code == 200:
            code = train_person_grp()
            if code == 202:
                return "success"
    return "failure"


def delete_employee_api(emp_id):
    person_id = get_personId(emp_id)
    if person_id != 'Try Again Later':
        code = delete_person(person_id)
        if code == 200:
            return "success"
    return 'failure'

