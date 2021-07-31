from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'POS'

urlpatterns = [

    ################# POS ################
    path('pos/', POSList.as_view(), name='POSList'),
    path('pos/new/', POSCreate.as_view(), name='POSCreate'),
    path('pos/trash/', POSTrashList.as_view(), name='POSTrashList'),
    path('pos/<int:pk>/show/', POSCard.as_view(), name='POSCard'),
    path('pos/EnterPOS/<int:id>', EnterPOS , name='EnterPOS'),
    path('pos/<int:pk>/delete/', POSDelete.as_view(), name='POSDelete'),
    path('pos/<int:pk>/edit/', POSUpdate.as_view(), name='POSUpdate'),
    path('pos/Report/<str:id>', PosReport , name="PosReport"),
    path('pos/xls', PosXls, name='PosXls'),
    path('pos_setting/', pos_setting, name='pos_setting'),
    ################# POS ################

    ################# SHIFTS ################
    path('shift/new/<int:pk>', ShiftCreate.as_view(), name='ShiftCreate'),
    path('shift/<int:pk>/show', ShiftCard.as_view(), name='ShiftCard'),
    path('EndShift/<str:id>', EndShift, name="EndShift"),
    path('shift/Report/<str:id>', Report, name="Report"),
    path('shiftWith/new/<int:pk>/<int:shiftId>', CreateShiftWithOrders.as_view(), name='CreateShiftWithOrders'),
    path('shift/<int:pk>/delete/<int:POSId>', ShiftDelete.as_view(), name='ShiftDelete'),
    ################# SHIFTS ################

    ################# ORDERS ################
    path('order/new/<int:pk>', OrderCreate.as_view(), name='OrderCreate'),
    path('OrderUpdate/<int:id>', OrderUpdate, name='OrderUpdate'),
    path('Orderdetail/<int:id>', Orderdetail, name='Orderdetail'),
    path('AddProduct/<str:o_id>/<str:id>/<str:q>', AddOrderdetail, name='AddProduct'),
    path('SingleProduct/<str:id>', SingleProduct, name='SingleProduct'),
    path('OrderTotalPrice/', OrderTotalPrice, name="OrderTotalPrice"),
    path('CheckOut/', CheckOut, name="CheckOut"),
    path('addDiscount/', view=addDiscount, name="addDiscount"),
    path('order/<int:pk>/edit/', OrderCustomerUpdate.as_view(), name='OrderCustomerUpdate'),
    path('CustomerAddress/<int:pk>/edit/', CustomerAddressUpdate.as_view(), name='CustomerAddressUpdate'),
    path('OrderCancel/<str:id>/<str:shiftid>', OrderCancel, name='OrderCancel'),
    path('OrderDelete/<int:pk>/', OrderDelete.as_view(), name="OrderDelete"),
    path('OrderPrintSetting/', PrintSetting , name='PrintSetting'),
    path('print/<int:pk>', printInvoice , name='print'),
    path('orderfloor/edit/<int:pk>/', OrderFloorUpdate.as_view(), name='OrderFloorUpdate'),
    path('orderTable/edit/<int:pk>/', OrderTabelUpdate.as_view(), name='OrderTabelUpdate'),
    path('OrderCreateByTabel/<int:s_id>/<int:t_id>', OrderCreateByTabel , name='OrderCreateByTabel'),
    path('Delete_order_detail/<int:id>/', Delete_order_detail , name="Delete_order_detail"),
    path('ChangeOrderDetailQuantity/', ChangeOrderDetailQuantity, name="ChangeOrderDetailQuantity"),
    path('addCustomerToOrder/<int:pk>/', add_customer_to_order , name="add_customer_to_order"),
    path('AddOrderDeliveryEmployee/<int:pk>', AddOrderDeliveryEmployee.as_view(), name="AddOrderDeliveryEmployee"),
    path('AddNewAddress/<int:pk>', AddNewAddress.as_view(), name="AddNewAddress"),
    path('addCustomerToOrder1/<int:pk>/<int:c_pk>/', add_customer_to_order1 , name="add_customer_to_order1"),
    path('add_customer_to_order_by_phone/<int:pk>/<int:p_pk>/', add_customer_to_order_by_phone , name="add_customer_to_order_by_phone"),
    ################# ORDERS ################

    ################# FLOOR ################
    path('floor/new/<int:pk>/', FloorCreate.as_view(), name='FloorCreate'),
    path('floor/delete/<int:pk>/', FloorDelete , name='FloorDelete'),
    ################# FLOOR ################

    ################# Table ################
    path('table/new/<int:pk>/', TableCreate.as_view(), name='TableCreate'),
    path('table/delete/<int:pk>/', TableDelete , name='TableDelete'),
    ################# Table ################

]