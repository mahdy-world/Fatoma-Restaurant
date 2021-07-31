from django.db import models
from Customers.models import Customer
from django.utils.timezone import now
from Auth.models import User
from Invoices.models import Invoice
from Calendar.models import Task


# Create your models here.
class ProjectStatus(models.Model):
    name = models.CharField(max_length=127, verbose_name='حالة المشروع')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_project_status', 'إضافة حالة مشروع'),
            ('edit_project_status', 'تعديل حالة مشروع'),
            ('delete_project_status', 'حذف حالة مشروع'),
            ('access_project_status_menu', 'الدخول علي قائمة حالات المشاريع'),
            ('download_project_status_data', 'تنزيل بيانات حالات المشاريع'),
        )


class Project(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم المشروع')
    client = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='العميل')
    start_date = models.DateField(default=now, verbose_name='تاريخ البدء')
    end_date = models.DateField(blank=True, null=True, verbose_name='تاريخ الإنتهاء')
    complete_percent = models.IntegerField(default=0, verbose_name='نسبة الإنجاز')
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, verbose_name='حالة المشروع')
    invoices = models.ManyToManyField(Invoice, verbose_name='فواتير المشروع')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_project', 'إضافة مشروع'),
            ('edit_project', 'تعديل مشروع'),
            ('delete_project', 'حذف مشروع'),
            ('view_project', 'عرض بيانات مشروع'),
            ('view_project_balance', 'عرض رصيد مشروع'),
            ('view_project_statement', 'كشف حساب مشروع'),
            ('access_project_menu', 'الدخول علي قائمة المشروعات'),
            ('download_project_data', 'تنزيل بيانات المشاريع'),
        )


class ProjectResponse(models.Model):
    response_type_choices = (
        (1, 'فاتورة'),
        (2, 'زيارة'),
        (3, 'موعد'),
        (4, 'مهام'),
        (5, 'ملف'),
        (6, 'مكالمة'),
        (7, 'تغيير حالة'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='المشروع')
    date = models.DateTimeField(default=now, verbose_name='التاريخ')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(choices=response_type_choices)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    visible_to_customer = models.BooleanField(default=False, verbose_name='ظهور للعميل')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True, verbose_name='ملاحظات')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('delete_project_response', 'حذف شريك'),
        )
