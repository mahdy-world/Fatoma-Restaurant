from .views import *
from django.urls import path


app_name = 'Partners'
urlpatterns = [
    path('', PartnerList.as_view(), name='PartnerList'),
    path('new/', PartnerCreate.as_view(), name='PartnerCreate'),
    path('trash/', PartnerTrashList.as_view(), name='PartnerTrashList'),
    path('<int:pk>/edit/', PartnerUpdate.as_view(), name='PartnerUpdate'),
    path('<int:pk>/delete/', PartnerDelete.as_view(), name='PartnerDelete'),
    path('xls', PartnerXls, name='PartnerXls'),
]