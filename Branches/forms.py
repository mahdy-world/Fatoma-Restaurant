from django import forms
from .models import *


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ['deleted']


class BranchDeleteForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['deleted']


class TreasuryForm(forms.ModelForm):
    class Meta:
        model = Treasury
        exclude = ['deleted']


class TreasuryDeleteForm(forms.ModelForm):
    class Meta:
        model = Treasury
        fields = ['deleted']