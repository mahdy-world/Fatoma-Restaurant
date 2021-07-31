from .views import *
from django.urls import path

app_name = 'Maintenance'
urlpatterns = [
    path('tickets/', TicketList.as_view(), name='TicketList'),
    path('tickets/new/', TicketCreate.as_view(), name='TicketCreate'),
    path('tickets/trash/', TicketTrashList.as_view(), name='TicketTrashList'),
    path('tickets/setting/', maintenance_print_setting, name='maintenance_print_setting'),
    path('tickets/<int:pk>/', TicketDetail.as_view(), name='TicketDetail'),
    path('tickets/<int:pk>/reply/', TicketReplyCreate.as_view(), name='TicketReplyCreate'),
    path('tickets/<int:pk>/done/', TicketDone.as_view(), name='TicketDone'),
    path('tickets/<int:pk>/reject/', RejectTicket.as_view(), name='RejectTicket'),
    path('tickets/<int:pk>/edit/', TicketUpdate.as_view(), name='TicketUpdate'),
    path('tickets/<int:pk>/delete/', TicketDelete.as_view(), name='TicketDelete'),
    path('tickets/<int:pk>/transfer/', TransferTo.as_view(), name='TransferTo'),
    path('tickets/<int:pk>/outsource/send/', OutsourceTransfer.as_view(), name='OutsourceTransfer'),
    path('tickets/<int:pk>/outsource/receive/', OutsourceReceived.as_view(), name='OutsourceReceived'),
    path('tickets/<int:pk>/diagnosis/', Diagnosis.as_view(), name='Diagnosis'),
    path('tickets/<int:pk>/cost/rating/', CostRating.as_view(), name='CostRating'),
    path('tickets/<int:pk>/customer/reply/', CustomerReply.as_view(), name='CustomerReply'),
    path('tickets/<int:pk>/customer/receive/', CustomerReceived.as_view(), name='CustomerReceived'),
    path('tickets/<int:pk>/print/receipt/', print_receipt, name='print_receipt'),
    path('tickets/xls', TicketXls, name='TicketXls'),
    ]
