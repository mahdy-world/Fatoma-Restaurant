from .views import *
from django.urls import path

app_name = 'Setting'
urlpatterns = [
    path('', setup, name='setup'),
    ]
