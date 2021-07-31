from django.urls import path
from .views import *

app_name = 'Auth'
urlpatterns = [
    path('users/login/', UserLogin.as_view(), name='UserLogin'),
    path('users/logout/', UserLogout.as_view(), name='UserLogout'),
    path('users/register/', RegisterUser.as_view(), name='RegisterUser'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('permissions/<int:pk>/', permissions, name='permissions'),
    path('login/as/<int:pk>/', login_as, name='login_as'),
    path('password/', change_password, name='change_password'),
    path('setting/', account_setting, name='account_setting'),
    path('users/<int:pk>/reset_password/', PasswordReset.as_view(), name='PasswordReset'),
    path('employee/<int:pk>/user/create/', create_user_for_employee, name='create_user_for_employee'),
]
