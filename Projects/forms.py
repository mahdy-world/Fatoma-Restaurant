from django import forms
from Projects.models import *


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = ProjectStatus
        exclude = ['deleted']


class ProjectStatusDeleteForm(forms.ModelForm):
    class Meta:
        model = ProjectStatus
        fields = ['deleted']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['invoices', 'end_date', 'deleted']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }


class ProjectDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['deleted']


class ChangeProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status', 'complete_percent']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }


class CallForm(forms.ModelForm):
    class Meta:
        model = ProjectResponse
        fields = ['comment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }