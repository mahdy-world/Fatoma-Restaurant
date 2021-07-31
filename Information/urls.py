from .views import *
from django.urls import path

app_name = 'Information'
urlpatterns = [
    path('information/', InformationList.as_view(), name='InformationList'),
    path('information/new/', InformationCreate.as_view(), name='InformationCreate'),
    path('information/<int:pk>/edit/', InformationUpdate.as_view(), name='InformationUpdate'),
    path('information/<int:pk>/show', InformationCard.as_view(), name='InformationCard'),
    path('information/<int:pk>/delete', DeleteInformation , name='DeleteInformation'),
    path('InformationXls', InformationXls, name='InformationXls'),

    path('information/category/', InformationCategoryList.as_view(), name='InformationCategoryList'),
    path('information/category/new/', InformationCategoryCreate.as_view(), name='InformationCategoryCreate'),
    path('information/category/<int:pk>/edit/', InformationCategoryUpdate.as_view(), name='InformationCategoryUpdate'),
    path('information/category/<int:pk>/delete', DeleteCategoryInformation, name='DeleteCategoryInformation'),
    path('InformationCategory/xls', InformationCategoryXls, name="InformationCategoryXls"),

]
