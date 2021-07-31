from .views import *
from django.urls import path

app_name = 'Customers'
urlpatterns = [
    path('categories/', CategoryList.as_view(), name='CategoryList'),
    path('categories/new/', CategoryCreate.as_view(), name='CategoryCreate'),
    path('categories/trash/', CategoryTrashList.as_view(), name='CategoryTrashList'),
    path('categories/<int:pk>/edit/', CategoryUpdate.as_view(), name='CategoryUpdate'),
    path('categories/<int:pk>/delete/', CategoryDelete.as_view(), name='CategoryDelete'),
    path('categories/xls', CategoryXls, name='CategoryXls'),
    
    
    path('customers/', CustomerList.as_view(), name='CustomerList'),
    path('customers/new/', CustomerCreate.as_view(), name='CustomerCreate'),
    path('customers/trash/', CustomerTrashList.as_view(), name='CustomerTrashList'),
    path('customers/<int:pk>/edit/', CustomerUpdate.as_view(), name='CustomerUpdate'),
    path('customers/<int:pk>/delete/', CustomerDelete.as_view(), name='CustomerDelete'),
    path('customers/<int:pk>/view/', CustomerDetail.as_view(), name='CustomerDetail'),
    path('customers/<int:pk>/invoices/', CustomerInvoices.as_view(), name='CustomerInvoices'),
    path('customers/<int:pk>/calls/', CustomerCalls.as_view(), name='CustomerCalls'),
    path('customers/xls', CustomerXls, name='CustomerXls'),


    path('customers/<int:pk>/calls/add/', add_call, name='add_call'),
    path('customers/calls/<int:pk>/view/', CallDetail.as_view(), name='CallDetail'),

    path('call_reasons/', CallReasonList.as_view(), name='CallReasonList'),
    path('call_reasons/new/', CallReasonCreate.as_view(), name='CallReasonCreate'),
    path('call_reasons/trash/', CallReasonTrashList.as_view(), name='CallReasonTrashList'),
    path('call_reasons/<int:pk>/edit/', CallReasonUpdate.as_view(), name='CallReasonUpdate'),
    path('call_reasons/<int:pk>/delete/', CallReasonDelete.as_view(), name='CallReasonDelete'),
    path('call_reasons/xls', CallReasonXls, name='CallReasonXls'),
    
    
    path('API/Customers/List/', CustomerAPIList.as_view(), name='CustomerAPIList'),
    path('API/Customers/<int:pk>/', CustomerAPIDetail.as_view(), name='CustomerAPIDetail'),

    ################### Address ##############################
    path('address/new/<int:pk>/', AddressCreate.as_view(), name='AddressCreate'),
    path('address/edit/<int:pk>/', AddressUpdate.as_view(), name='AddressUpdate'),
    path('address/delete/<int:pk>/', AddressDelete, name="AddressDelete"),
    ################### Address ##############################

    path('group/', GroupList.as_view(), name='GroupList'),
    path('group/trash/', GroupTrashList.as_view(), name='GroupTrashList'),
    path('group/new/', GroupCreate.as_view(), name='GroupCreate'),
    path('group/<int:pk>/edit/', GroupUpdate.as_view(), name='GroupUpdate'),
    path('group/<int:pk>/delete/', GroupDelete.as_view(), name='GroupDelete'),
    path('group/xls', GroupXls, name='GroupXls'),

    ################### Phone ##############################
    path('phone/new/<int:pk>/', PhoneCreate.as_view(), name='PhoneCreate'),
    path('phone/edit/<int:pk>/', PhoneUpdate.as_view(), name='PhoneUpdate'),
    path('phone/delete/<int:pk>/', PhoneDelete , name="PhoneDelete"),
    ################### Phone ##############################
]