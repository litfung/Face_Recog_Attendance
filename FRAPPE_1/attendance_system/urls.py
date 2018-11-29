from django.conf.urls import url
from . import views


app_name = 'attendance_system'
urlpatterns = [

# /mark
    url(r'^$', views.RecogniseEmployee.as_view(), name='rec-emp'),

    # /mark
    url(r'^mark/$', views.MarkAttendance.as_view(), name='mark-attendance'),

    # /raise_alert
    url(r'^raise_alert/$', views.RaiseAlert.as_view(), name='raise_alert'),
]