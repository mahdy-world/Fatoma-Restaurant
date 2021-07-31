from django import forms
from Auth.models import *
from Invoices.models import *
from django.utils.timezone import now
from Maintenance.models import *


class InvoiceReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1).isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    creator = forms.ModelChoiceField(queryset=User.objects.all(), label='أصدر بواسطة', required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(deleted=False), label='الفرع', required=False)
    treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة', required=False)


class ExpenseReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1).isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    creator = forms.ModelChoiceField(queryset=User.objects.all(), label='أصدر بواسطة', required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(deleted=False), label='الفرع', required=False)
    treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة', required=False)
    spend_category = forms.ModelChoiceField(queryset=SpendCategory.objects.filter(deleted=False), label='التصنيف',
                                            required=False)


class ProfitReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1).isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    invoice_type = forms.ChoiceField(choices=(
        (1, 'فاتورة مبيعات'),
        (2, 'فاتورة مبيعات توصيل'),
        (3, 'فاتورة مبيعات موقع'),
        (4, 'فاتورة مرتجع مبيعات'),)
    )
    creator = forms.ModelChoiceField(queryset=User.objects.all(), label='أصدر بواسطة', required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(deleted=False), label='الفرع', required=False)
    treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة', required=False)


class TreasuryBalanceReportForm(forms.Form):
    treasury = forms.ModelMultipleChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة',
                                              required=False)


class TreasuryReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة', required=True)

class DailyRestrictionsForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())

class ItemStockReportForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Product.objects.all(), label='المنتج')
    branch = forms.ModelMultipleChoiceField(queryset=Branch.objects.filter(deleted=False), label='المخزن',
                                            required=False)


class ItemTransactionReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    item = forms.ModelChoiceField(queryset=Product.objects.all(), label='المنتج', required=False)
    branch = forms.ModelMultipleChoiceField(queryset=Branch.objects.filter(deleted=False), label='المخزن',
                                            required=False)


class BranchStockReportForm(forms.Form):
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(deleted=False), label='المخزن', required=True)


class CustomerStatementReportFrom(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(deleted=False), label='العميل/المورد')
    report_type = forms.ChoiceField(choices=((1, 'مختصر'), (2, 'تفصيلي')), label='نوع كشف الحساب')


class ProfitLossReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())


class MaintenanceReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().isoformat())
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي',
                              initial=now().date().isoformat())
    product = forms.ModelChoiceField(queryset=Product.objects.filter(deleted=False), label='المنتج', required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(deleted=False), label='العميل', required=False)
    outsource_status = forms.ChoiceField(label='حالة الصيانة الخارجية', initial=0, choices=(
        (0, 'جميع التذاكر'),
        (1, 'صيانة داخلية'),
        (2, 'صيانة خارجية لم تستلم بعد'),
        (3, 'صيانة خارجية تم استلامها'),
    ))
    ticket_status = forms.ChoiceField(label='حالة التذكرة', initial=0, choices=(
        (0, 'جميع التذاكر'),
        (1, 'قيد التشخيص'),
        (2, 'قيد التقييم'),
        (3, 'في انتظار رد العميل'),
        (4, 'العميل يرفض التكلفة'),
        (5, 'العميل يرفض فترة الإصلاح'),
        (6, 'قيد الإصلاح'),
        (7, 'تمت الصيانة'),
        (8, 'لا يمكن الإصلاح')
    ))
    ticket_type = forms.ChoiceField(label='نوع التذكرة', initial=0, choices=(
        (0, 'جميع التذاكر'),
        (1, 'صيانة'),
        (2, 'ضمان'),
    ))
    customer_receive_status = forms.ChoiceField(label='حالة استلام العميل', initial=0, choices=(
        (0, 'جميع التذاكر'),
        (1, 'العميل استلم'),
        (2, 'العميل لم يستلم'),
    ))


class NotSoldItemsForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='منتجات لم تباع منذ',
                           initial=now().date().replace(day=1))
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(deleted=False), label='المخزن', required=True)


class PartnersPercentForm(forms.Form):
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='في تاريخ', initial=now().date())


class PartnerTransactionForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي', initial=now().date())
    partner = forms.ModelChoiceField(queryset=Partner.objects.filter(deleted=False), label='الشريك', required=False)


class EmployeeReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي', initial=now().date())
    employee = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_staff=True), label='الموظف',
                                      required=True)


class NewCustomersForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='من',
                                initial=now().date().replace(day=1))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='إلي', initial=now().date())
    employee = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_staff=True), label='الموظف',
                                      required=False)