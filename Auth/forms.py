from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.TextInput()
    password = forms.PasswordInput()


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['allowed_branches', 'allowed_treasuries', 'default_branch', 'default_treasury', 'is_superuser', 'user_permissions']


class UserDisableForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]


class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'password',
        ]


class AccountSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'default_branch',
            'default_treasury',
        ]


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }