from django import forms
from .models import *


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        exclude = ['deleted']

class InformationCategoryForm(forms.ModelForm):
    class Meta:
        model = InformationCategory
        exclude = ['deleted']