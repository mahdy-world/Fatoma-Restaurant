from .views import *
from django.urls import path

app_name = 'HR'
urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='EmployeeList'),
    path('employees/new/', EmployeeCreate.as_view(), name='EmployeeCreate'),
    path('employees/<int:pk>/edit/', EmployeeUpdate.as_view(), name='EmployeeUpdate'),
    path('employees/<int:pk>/delete/', EmployeeDelete.as_view(), name='EmployeeDelete'),
    path('employees/<int:pk>/view/', EmployeeDetail.as_view(), name='EmployeeDetail'),
    path('employees/<int:pk>/upload/', UploadFile.as_view(), name='UploadFile'),
    path('employees/files/view/<int:pk>/', ViewFile.as_view(), name='ViewFile'),
    path('employee/xls', EmployeeXls, name='EmployeeXls'),

    path('job_title/', JobTitleList.as_view(), name='JobTitleList'),
    path('job_title/new/', JobTitleCreate.as_view(), name='JobTitleCreate'),
    path('job_title/<int:pk>/edit/', JobTitleUpdate.as_view(), name='JobTitleUpdate'),
    path('job_title/<int:pk>/delete/', JobTitleDelete.as_view(), name='JobTitleDelete'),
    path('job_title/xls', JobTitleXls, name='JobTitleXls'),
    ]