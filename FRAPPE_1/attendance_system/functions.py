import datetime
import pytz
from .face_functions import detect, identify, get_person
from management_system.models import AttendanceLog

local_tz = pytz.timezone('Asia/Kolkata')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def current_date():
    now = datetime.datetime.now()
    now = utc_to_local(now)
    return now.strftime("%d-%m-%Y")


def current_time():
    now = datetime.datetime.now()
    now = utc_to_local(now)
    return now.strftime("%H:%M:%S")


def day_diff(initial_date,final_date):
    date_format = "%d-%m-%Y"
    a = datetime.datetime.strptime(initial_date, date_format)
    b = datetime.datetime.strptime(final_date, date_format)
    a = utc_to_local(a)
    b = utc_to_local(b)
    delta = b - a
    return (delta.days+1)


def date_array(initial_date, final_date):
    datearray = []
    date_format = "%d-%m-%Y"
    a = datetime.datetime.strptime(initial_date, date_format)
    b = datetime.datetime.strptime(final_date, date_format)
    a = utc_to_local(a)
    b = utc_to_local(b)
    delta = b - a
    for i in range(delta.days + 1):
        date = a + datetime.timedelta(i)
        datearray.append(date.strftime('%d-%m-%Y'))

    return datearray


# Face Recognition
def face_recognise(path):
    facelist = detect(path)
    if facelist is not None:
        person_id = identify(facelist)
        if person_id != "Try Again Later":
            emp_id = get_person(person_id)
            return emp_id
    else:
        return -1


def getLatestLog():
    key = AttendanceLog.objects.all()[AttendanceLog.objects.all().count()-1].employee.emp_id
    return key