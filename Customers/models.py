from django.db import models
from django.db.models import Count, Sum
from django.db.models import F, FloatField, Sum
from Auth.models import User
from django.db.models.signals import post_save, pre_save





# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_customer_category', 'إضافة شريحة عملاء'),
            ('edit_customer_category', 'تعديل شريحة عملاء'),
            ('delete_customer_category', 'حذف شريحة عملاء'),
            ('access_customer_category_menu', 'الدخول علي قائمة شرائح العملاء'),
            ('download_customer_category_data', 'تنزيل بيانات شرائح العملاء')
        )

class CustomerGroup(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_customer_rating', 'إضافة تصنيف عملاء'),
            ('edit_customer_rating', 'تعديل تصنيف عملاء'),
            ('delete_customer_rating', 'حذف تصنيف عملاء'),
            ('access_customer_rating_menu', 'الدخول علي قائمة تصنيفات العملاء'),
            ('download_customer_rating_data', 'تنزيل بيانات تصنيفات العملاء')
        )

class Customer(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    facebook_account = models.CharField(max_length=128, verbose_name='حساب الفيس بوك', null=True, blank=True)
    job = models.CharField(max_length=128, null=True, blank=True, verbose_name='الوظيفة')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الشريحة')
    group = models.ForeignKey(CustomerGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='التصنيف')
    initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    allow_negative_balance = models.BooleanField(default=False, verbose_name='السماح بالبيع آجل')
    max_negative_balance = models.FloatField(default=0.0, verbose_name='الحد الإئتماني')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='اضيف بواسطة')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='أضيف بتاريخ')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    def balance(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(total=Sum(F('customer_debit'), output_field=FloatField()) - Sum(F('customer_credit'), output_field=FloatField()), debit=Sum('customer_debit'), credit=Sum('customer_credit'))
        if not balance['total']:
            return self.initial_balance
        else:
            return balance['total'] + self.initial_balance

    def total_debit(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(debit=Sum('customer_debit'))
        if self.initial_balance > 0:
            if not balance['debit']:
                return self.initial_balance
            else:
                return balance['debit'] + self.initial_balance
        else:
            if not balance['debit']:
                return 0
            else:
                return balance['debit']

    def total_credit(self):
        invoices = self.invoice_set.filter(deleted=False, saved=True)
        balance = invoices.aggregate(credit=Sum('customer_credit'))
        if self.initial_balance < 0:
            if not balance['credit']:
                return self.initial_balance
            else:
                return balance['credit'] - self.initial_balance
        else:
            if not balance['credit']:
                return 0
            else:
                return balance['credit']

    def is_creditor(self):
        if self.balance():
            if self.balance() < 0:
                return True
            else:
                return False

    def is_debitor(self):
        if self.balance():
            if self.balance() > 0:
                return True
            else:
                return False

    def sales_invoices(self):
        return self.invoice_set.filter(deleted=False, invoice_type=1)

    def quotations(self):
        return self.invoice_set.filter(deleted=False, invoice_type=7)

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_customer', 'إضافة عميل/مورد'),
            ('edit_customer', 'تعديل عميل/مورد'),
            ('delete_customer', 'حذف عميل/مورد'),
            ('view_customer', 'عرض بيانات عميل/مورد'),
            ('view_customer_balance', 'عرض رصيد عميل/مورد'),
            ('view_customer_statement', 'كشف حساب عميل/مورد'),
            ('access_customer_menu', 'الدخول علي قائمة العملاء/الموردين'),
            ('download_customer_data', 'تنزيل بيانات العملاء'),
            ('access_customer_account_statement','الدخول على كشف حساب عميل/مورد'),
            ('access_creditors_report','الدخول على تقرير الدائنون (له)'),
            ('access_debtors_report','الدخول على تقرير المدينون (عليه)'),
            ('access_idle_customer_report','الدخول على تقارير العملاء الخاملين'),
            ('access_customer_report','الدخول على تقارير العملاء/الموردين'),
            ('access_customer_best_seller_report','الدخول على تقارير العملاء/الموردين الأكثر مبيعاً'),

        )


class CustomerNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    title = models.CharField(max_length=128, verbose_name='عنوان الملاحظات')
    note = models.TextField(verbose_name='محتوي الملاحظة')

    def __str__(self):
        return self.title


class CallReason(models.Model):
    name = models.CharField(verbose_name='سبب الإتصال', max_length=128)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_call_reason', 'إضافة سبب إتصال '),
            ('edit_call_reason', 'تعديل سبب إتصال'),
            ('delete_call_reason', 'حذف سبب إتصال'),
            ('access_call_reason_menu', 'الدخول علي قائمة أسباب الإتصال'),
            ('download_call_reason_data', 'تنزيل بيانات أسباب الإتصال')
        )


class CustomerCall(models.Model):
    call_type_choices = (
        (1, 'مكالمة صادرة'),
        (2, 'مكالمة واردة'),
        (3, 'Whatsapp'),
        (4, 'Messenger')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    call_type = models.IntegerField(choices=call_type_choices, verbose_name='نوع المكالمة')
    call_reason = models.ForeignKey(CallReason, on_delete=models.SET_NULL, null=True, verbose_name='سبب المكالمة')
    summary = models.TextField(verbose_name='ملخص المكالمة')

    def __str__(self):
        return self.summary
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_customer_call', 'إضافة مكالمة '),
            ('edit_customer_call', 'تعديل مكالمة'),
            ('delete_customer_call', 'حذف مكالمة'),
            ('access_customer_call_menu', 'الدخول علي قائمة المكالمات'),
        )


class CustomerHistory(models.Model):
    history_type_choices = (
        (1, 'إضافة عميل'),
        (2, 'إضافة مكالمة'),
        (3, 'إضافة عرض سعر'),
        (4, 'إضافة فاتورة مبيعات'),
        (5, 'إضافة فاتورة مرتجع مبيعات'),
        (6, 'إضافة فاتورة مشتريات'),
        (7, 'إضافة فاتورة مرتجع مشتريات'),
        (8, 'إضافة ملاحظة'),
        (9, 'إضافة مكالمة'),
        (10, 'تحديد مهام'),
    )
    history_type = models.IntegerField(choices=history_type_choices, verbose_name='نوع العملية')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='العميل')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الموظف')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    call = models.ForeignKey(CustomerCall, on_delete=models.CASCADE, verbose_name='المكالمة', null=True)
    note = models.ForeignKey(CustomerNote, on_delete=models.CASCADE, verbose_name='الملاحظة', null=True)
    invoice_id = models.IntegerField(verbose_name='رقم الفاتورة', null=True)

    def __str__(self):
        return self.get_history_type_display()

    class Meta:
        ordering = ['-added_at']


def save_customer(sender, instance, created, **kwargs):
    if created:
        history = CustomerHistory()
        history.added_by = instance.added_by
        history.added_at = instance.added_at
        history.history_type = 1
        history.customer = instance
        history.save()


post_save.connect(save_customer, sender=Customer)


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='الموظف')
    country = models.CharField(max_length=150, null=True, blank=True, verbose_name='الدولة')
    country_delivery_cost = models.FloatField(default=0, verbose_name='سعر توصيل الدولة')
    region = models.CharField(max_length=150, null=True, blank=True, verbose_name='الإقليم')
    governorate = models.CharField(max_length=150, null=True, blank=True, verbose_name='المحافظة')
    governorate_delivery_cost = models.FloatField(default=0, verbose_name='سعر توصيل المحافظة')
    area = models.CharField(max_length=150, null=True, blank=True, verbose_name='المنطقة')
    area_delivery_cost = models.FloatField(default=0, verbose_name='سعر توصيل المنطقة')
    address = models.TextField(null=True, blank=True, verbose_name='العنوان')

    def __str__(self):
        return str(self.country) + str(',') + str(self.governorate) + str(',') + str(self.area) + str(',') + str(self.address)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_address', 'إضافة عنوان '),
            ('edit_address', 'تعديل عنوان'),
            ('delete_address', 'حذف عنوان'),
            ('access_address_menu', 'الدخول علي قائمة العناوين'),
        )

class Phone(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='الموظف')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='رقم الموبايل')

    def __str__(self):
        return str(self.phone)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_customer_phone', 'إضافة رقم العميل / المورد '),
            ('edit_customer_phone', 'تعديل رقم العميل / المورد'),
            ('delete_customer_phone', 'حذف رقم العميل / المورد'),
            ('access_customer_phone_menu', 'الدخول علي قائمة ارقام الموظف'),
        )