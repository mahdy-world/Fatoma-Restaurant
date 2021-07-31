from django.db import models
from django.db.models import F, FloatField, Sum
from datetime import date


# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم الشريك')
    phone = models.CharField(max_length=11, verbose_name='رقم الهاتف')
    initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def balance(self, from_date="1970-01-01", to_date="2100-12-31"):
        invoices = self.invoice_set.filter(deleted=False, date__date__gte=from_date, date__date__lte=to_date)
        balance = invoices.aggregate(total=Sum(F('treasury_in'), output_field=FloatField()) - Sum(F('treasury_out'), output_field=FloatField()), debit=Sum('treasury_in'), credit=Sum('treasury_out'))
        if invoices.count() > 0:
            return balance['total'] + self.initial_balance
        else:
            return self.initial_balance

    def percent(self, from_date="1970-01-01", to_date="2100-12-31"):
        my_invoices_total = self.balance(from_date, to_date)
        total = self.initial_balance
        for x in Partner.objects.filter(deleted=False):
            total += x.balance(from_date, to_date)
        if not total == 0:
            percent = (100 * my_invoices_total) / total
            return percent
        else:
            return self.initial_balance

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_partner', 'إضافة شريك'),
            ('edit_partner', 'تعديل شريك'),
            ('delete_partner', 'حذف شريك'),
            ('view_partner', 'عرض بيانات شريك'),
            ('view_partner_balance', 'عرض رصيد شريك'),
            ('view_partner_statement', 'كشف حساب شريك'),
            ('access_partner_menu', 'الدخول علي قائمة الشركاء'),
            ('download_partner_data' , 'تنزيل بيانات الشركاء'),
            ('access_partners_balances_report','الدخول على نسب وأرصدة الشركاء'),
            ('access_capital_movements_report','الدخول على تقرير حركات رأس المال'),
        )
