from django import forms
from django.forms import fields
from .models import *
from Invoices.models import *


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['quantity']

class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = '__all__'

        widgets = {
            'index_text': forms.Textarea(attrs={'rows': '2'}),
            'about_text': forms.Textarea(attrs={'rows': '2'}),
            'about_statistics_text': forms.Textarea(attrs={'rows': '2'}),
            'service_text': forms.Textarea(attrs={'rows': '2'}),
            'product_text': forms.Textarea(attrs={'rows': '2'}),
            'team_text': forms.Textarea(attrs={'rows': '2'}),
            'call_text': forms.Textarea(attrs={'rows': '2'}),
        }

class AboutItemsForm(forms.ModelForm):
    class Meta:
        model = AboutItems
        fields = '__all__'

class StatisticsItemsForm(forms.ModelForm):
    class Meta:
        model = StatisticsItems
        fields = '__all__'

class ServiceItemsForm(forms.ModelForm):
    class Meta:
        model = ServiceItems
        fields = '__all__'

class ProductItemsForm(forms.ModelForm):
    class Meta:
        model = ProductItems
        fields = '__all__'

class TeamItemsForm(forms.ModelForm):
    class Meta:
        model = TeamItems
        fields = '__all__'
