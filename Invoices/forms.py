from django import forms

from .models import *


class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'treasury_in',
            'overall',
            'comment',
            'internal_comment',
        ]
        labels = {
            'treasury_in': 'مدفوع',
        }
        widgets = {
            'total': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'shipping': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'invoice_type': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'overall': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }


class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'treasury_out',
            'overall',
            'comment',
            'internal_comment',
        ]
        labels = {
            'treasury_out': 'مدفوع',
        }
        widgets = {
            'total': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'shipping': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'invoice_type': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'overall': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }


class PlusMinusForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'comment',
            'internal_comment',
        ]


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['overall', 'comment', 'internal_comment']


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['invoice', 'cost_profit', 'purchase_profit']


class InvoiceDeleteForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['deleted']


class InvoiceItemPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['unit_price']


class InvoiceItemQuantityUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['quantity']


class InvoiceItemDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['discount']


class InvoiceDateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class InvoiceDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['discount']


class InvoiceCustomerForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']


class InvoiceToBranchForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['to_branch']


class InvoiceFromBranchForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['from_branch']


class InvoiceFromTreasuryForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['from_treasury']


class InvoiceToTreasuryForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['to_treasury']


class InvoiceUnSaveForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['saved']


class ExpenseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'spend_category', 'treasury_out', 'from_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    spend_category = forms.ModelChoiceField(queryset=SpendCategory.objects.filter(deleted=False), label='تصنيف المصروفات')
    from_treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='من خزينة')


class IncomeInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'spend_category', 'treasury_in', 'to_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    spend_category = forms.ModelChoiceField(queryset=SpendCategory.objects.filter(deleted=False), label='تصنيف القبض')
    to_treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='إلي خزينة')


class SettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceSetting
        fields = '__all__'


class BaseSettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceBaseSetting
        fields = '__all__'


class CustomerOutcomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer', 'treasury_out', 'from_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CustomerIncomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer', 'treasury_in', 'to_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CapitalOutcomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'partner', 'treasury_out', 'from_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CapitalIncomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'partner',  'treasury_in', 'to_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class SpendCategoryForm(forms.ModelForm):
    class Meta:
        model = SpendCategory
        exclude = ['deleted']


class SpendCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = SpendCategory
        fields = ['deleted']


class BranchTransferForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'from_branch',
            'to_branch',
        ]


class StockTransferSaveForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'comment',
            'internal_comment',
        ]


class TreasuryTransferForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'date',
            'from_treasury',
            'to_treasury',
            'treasury_in',
            'comment',
        ]
        labels = {
            'treasury_in': 'المبلغ',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class DailyRestrictionsForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'date',
            'from_treasury',
            'to_treasury',
            'treasury_in',
            'comment',
        ]
        labels = {
            'from_treasury':'مدين',
            'to_treasury':'دائن',
            'treasury_in': 'المبلغ',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
