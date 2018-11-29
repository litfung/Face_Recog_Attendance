from django.conf.urls import url
from . import views


app_name = 'management_system'
urlpatterns = [
    # /mgmt/logout/
     url(r'^logout/$', views.logout_view, name='logout'),

    # /mgmt/
    url(r'^$', views.LoginView.as_view(), name='login'),

    # /mgmt/emp/
    url(r'^emp/$', views.EmployeeDetails.as_view(), name="emp-detail"),

    # /mgmt/admin/
    url(r'^admin/$', views.AdminDetails.as_view(), name="admin-detail"),

    # /mgmt/emp/update/
    url(r'^emp/update/$', views.UpdateDetails.as_view(), name="update"),

    # /mgmt/emp/check_attendance/
    url(r'^emp/check_attendance/$', views.ViewAttendanceRecords.as_view(), name="check-attendance"),

    # /mgmt/admin/attendance_record/
    url(r'^admin/attendance_record/$', views.AViewAttendanceRecords.as_view(), name="attendance-record"),

    # /mgmt/admin/alerts/
    url(r'^admin/alerts/$', views.AAlerts.as_view(), name="alerts"),

    # /mgmt/admin/update/
    url(r'^admin/update/$', views.AUpdateDetails.as_view(), name="a-update"),

    # /mgmt/emp/chpwd/
    url(r'^emp/chpwd/$', views.PwdChange.as_view(), name="change-password"),

    # /mgmt/admin/chpwd/
    url(r'^admin/chpwd/$', views.APwdChange.as_view(), name="a-change-password"),

    # /mgmt/admin/delete
    url(r'^admin/delete/$', views.DeleteEmployee.as_view(), name="remove-employee"),

    # /mgmt/admin/add/
    url(r'^admin/add/$', views.AddEmployee.as_view(), name="add-employee"),

    # /mgmt/admin/register
    url(r'^admin/register/$', views.RegisterView.as_view(), name="register-user"),

]
