from django import forms
from .models import *


class SetupForm(forms.ModelForm):
    class Meta:
        model = ModulesSetting
        fields = '__all__'


class EditModulesForm(forms.ModelForm):
    class Meta:
        model = ModulesSetting
        fields = '__all__'