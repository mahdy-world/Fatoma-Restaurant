from django import forms
from Partners.models import *


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        exclude = ['deleted']


class PartnerDeleteForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['deleted']

