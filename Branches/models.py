from django.db import models

class Branch(models.Model):
    types = (
        (1, 'فرع'),
        (2, 'مخزن'),
    )
    type = models.IntegerField(choices=types, verbose_name='النوع')
    name = models.CharField(max_length=128, verbose_name='الاسم')
    address = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    phone = models.CharField(max_length=128, verbose_name='التليفون', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_branch', 'إضافة فرع'),
            ('edit_branch', 'تعديل فرع'),
            ('delete_branch', 'حذف فرع'),
            ('access_branch_menu', 'الدخول علي قائمة الفروع'),
            ('download_branch_data','تنزيل بيانات الفروع'),
            ('access_product_stock_balance_report','الدخول على تقرير رصيد مخزون منتج'),
            ('access_product_movement_report','الدخول على تقرير حركة منتج'),
            ('access_branch_inventory_report','الدخول على تقرير جرد مخزن'),
            ('access_items_on_demand_report','الدخول على تقرير أصناف تحت حد الطلب'),
            ('access_items_on_critical_balance_report','الدخول على تقرير أصناف وصلت للرصيد الحرج'),
            ('access_stagnant_report','الدخول على تقرير الرواكد'),
        )


class Treasury(models.Model):
    types = (
        (1, 'خزينة'),
        (2, 'حساب بنكي'),
        (3, 'حساب عهدة'),
        (4, 'حساب سلف رواتب'),
    )
    type = models.IntegerField(choices=types, verbose_name='النوع')
    name = models.CharField(max_length=128, verbose_name='الاسم')
    no = models.CharField(max_length=128, verbose_name='رقم الحساب', null=True, blank=True)
    initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def balance(self):
        in_invoices = self.treasury_in_transactions.filter(saved=True, deleted=False)
        out_invoices = self.treasury_out_transactions.filter(saved=True, deleted=False)
        balance = self.initial_balance
        for invoice in in_invoices:
            balance += invoice.treasury_in
        for invoice in out_invoices:
            balance -= invoice.treasury_out
        return balance

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_treasury', 'إضافة خزينة و حساب بنكي'),
            ('edit_treasury', 'تعديل خزينة و حساب بنكي'),
            ('delete_treasury', 'حذف خزينة و حساب بنكي'),
            ('access_treasury_menu', 'الدخول علي قائمة الخزائن والحسابات البنكية'),
            ('download_treasury_data','تنزيل بيانات الخزائن'),
            ('access_treasury_balances_report','الدخول لتقرير أرصدة الخزائن'),
            ('access_treasury_moves_report','الدخول على تقرير حركات الخزائن'),
        )
