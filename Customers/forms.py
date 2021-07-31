from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['deleted']


class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['deleted']
        
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['deleted']
        widgets = {
            'added_by': forms.HiddenInput(),
        }


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['deleted', 'added_by']


class CustomerDeleteForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['deleted']


class CallReasonForm(forms.ModelForm):
    class Meta:
        model = CallReason
        exclude = ['deleted']


class CallReasonDeleteForm(forms.ModelForm):
    class Meta:
        model = CallReason
        fields = ['deleted']


class CustomerCallForm(forms.ModelForm):
    class Meta:
        model = CustomerCall
        fields = ['call_type', 'call_reason', 'summary']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['customer']

class AddressForm1(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['customer', 'country_delivery_cost', 'governorate_delivery_cost']

class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomerGroup
        exclude = ['deleted']

class GroupDeleteForm(forms.ModelForm):
    class Meta:
        model = CustomerGroup
        fields = ['deleted']

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ['customer']