from .views import *
from django.urls import path


app_name = 'Projects'
urlpatterns = [
    path('status/', ProjectStatusList.as_view(), name='ProjectStatusList'),
    path('status/new/', ProjectStatusCreate.as_view(), name='ProjectStatusCreate'),
    path('status/trash/', ProjectStatusTrashList.as_view(), name='ProjectStatusTrashList'),
    path('status/<int:pk>/edit/', ProjectStatusUpdate.as_view(), name='ProjectStatusUpdate'),
    path('status/<int:pk>/delete/', ProjectStatusDelete.as_view(), name='ProjectStatusDelete'),
    path('', ProjectList.as_view(), name='ProjectList'),
    path('new/', ProjectCreate.as_view(), name='ProjectCreate'),
    path('trash/', ProjectTrashList.as_view(), name='ProjectTrashList'),
    path('<int:pk>/edit/', ProjectUpdate.as_view(), name='ProjectUpdate'),
    path('<int:pk>/delete/', ProjectDelete.as_view(), name='ProjectDelete'),
    path('<int:pk>/view/', ProjectView.as_view(), name='ProjectView'),
    path('<int:pk>/status/change/', change_project_status, name='change_project_status'),
    path('status/xls', ProjectStatusXls , name='ProjectStatusXls'),
    path('project/xls', ProjectXls , name='ProjectXls'),
]