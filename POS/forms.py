from django import forms
from django.db.models import fields
from .models import *

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        exclude = ['createdBy','deleted']

class POSDeleteForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['deleted']

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'
        exclude = ['pos','status','deleted','invoice','end_time']

class ShiftDeleteForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['deleted']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['customer']

class OrderFloorForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['floor']

class OrderTabelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['table']

class OrderDeleteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['deleted']

class CustomerAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['address']

class PosSettingForm(forms.ModelForm):
    class Meta:
        model = PosBaseSetting
        fields = '__all__'

class OrderPrintForm(forms.ModelForm):
    class Meta:
        model = OrderPrintSetting
        fields  = '__all__'

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        exclude = ['pos']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name']

class OrderDeliveryEmployeeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields  = ['delivery_employees']