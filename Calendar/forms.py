from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'date',
            'task_type',
            'related_to',
            'employee',
            'comment',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class TaskDoneForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'done'
        ]


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'deleted'
        ]


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'date',
            'related_to',
            'comment'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class TaskTransferForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['employee']


class ChangeTaskTypeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type']


class RemoveTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'deleted',
        ]


class TaskRespondForm(forms.ModelForm):
    class Meta:
        model = TaskRespond
        fields = ['comment']

