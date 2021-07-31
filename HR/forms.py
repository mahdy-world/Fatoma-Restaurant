from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import *


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['deleted', 'user']
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'datepicker'}),
            'settlement_end_date': AdminDateWidget(),
            'insurance_start': AdminDateWidget(),
            'insurance_end': AdminDateWidget(),
            'start_date': AdminDateWidget(),
            'end_date': AdminDateWidget(),
        }


class EmployeeDeleteForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ['deleted']


class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        exclude = ['deleted']


class JobTitleDeleteForm(forms.ModelForm):
        class Meta:
            model = JobTitle
            fields = ['deleted']


class EmployeeFileForm(forms.ModelForm):
        class Meta:
            model = EmployeeFile
            fields = ['file']
            widgets = {
                'employee': forms.HiddenInput(),
            }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]