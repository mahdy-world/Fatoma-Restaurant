from .views import *
from django.urls import path

app_name = 'Barcode'
urlpatterns = [
        path('generator/single/<int:barcode>/', barcode_generator, name='single_generator'),
        path('view/', view_barcode, name='view_barcode'),
        path('print/', print_barcode, name='print_barcode'),
        path('setting/', barcode_setting, name='barcode_setting'),
        path('print/invoice/<int:pk>/', print_barcode_for_invoice, name='print_barcode_for_invoice'),
        ]