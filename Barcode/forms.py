from django import forms
from .models import *


class SettingForm(forms.ModelForm):
    class Meta:
        model = BarcodeSetting
        fields = '__all__'