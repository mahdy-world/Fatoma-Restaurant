from django.urls import path
from .views import *


app_name = 'Calendar'
urlpatterns = [
    path('create/', TaskCreate.as_view(), name='TaskCreate'),
    path('trash/', TaskTrashList.as_view(), name='TaskTrashList'),
    path('view/<int:pk>/', TaskView.as_view(), name='TaskView'),
    path('edit/<int:pk>/', TaskUpdate.as_view(), name='TaskUpdate'),
    path('done/<int:pk>/', TaskDone.as_view(), name='TaskDone'),
    path('transfer/<int:pk>/', TaskTransfer.as_view(), name='TaskTransfer'),
    path('delete/<int:pk>/', TaskDelete.as_view(), name='TaskDelete'),
    path('all/', TaskList.as_view(), name='TaskList'),
    path('calendar/xls', TaskXls, name='TaskXls'),

]