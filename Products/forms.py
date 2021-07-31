from django import forms
from django.db.models import fields
from .models import *


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        exclude = ['deleted']


class MainCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['deleted']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        exclude = ['deleted']


class SubCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['deleted']
        

class ManufactureForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        exclude = ['deleted']


class ManufactureDeleteForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        fields = ['deleted']
        

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = ['deleted']


class BrandDeleteForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['deleted']
        

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['deleted']


class UnitDeleteForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['deleted']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['sub_unit','sub_sub_unit','amount_in_sub_unit','amount_in_sub_sub_unit','deleted']
        widgets = {
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['deleted']


class GroupedProductForm(forms.ModelForm):
    class Meta:
        model = GroupedProduct
        exclude = ['grouped_item']

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = '__all__'


class PricesProductFormU(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['price', 'discount', 'opration', 'order']


class PricesProductFormD(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['deleted']

class PricesProductFormS(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['inactive']