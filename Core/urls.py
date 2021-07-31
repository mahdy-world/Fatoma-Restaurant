from .views import *
from django.urls import path

app_name = 'Core'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('change_log/', ChangeLog.as_view(), name='ChangeLog'),
    path('fix/', fix, name='fix'),
    path('update/', update, name='update'),
]
