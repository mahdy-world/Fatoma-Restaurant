from django.db import models
from django.utils.timezone import now

from Auth.models import User
from Customers.models import Customer
from Products.models import Product


# Create your models here.
class Ticket(models.Model):
    status_choices = (
        (1, 'قيد التشخيص'),
        (2, 'قيد التقييم'),
        (3, 'في انتظار رد العميل'),
        (4, 'العميل يرفض التكلفة'),
        (5, 'العميل يرفض فترة الإصلاح'),
        (6, 'قيد الإصلاح'),
        (7, 'تمت الصيانة'),
        (8, 'لا يمكن الإصلاح')
    )
    outsource_status_choices = (
        (1, 'صيانة داخلية'),
        (2, 'تم تحويلها لصيانة خارجية'),
        (3, 'تم استلامها من الصيانة الخارجية'),
    )
    customer_reply_choices = (
        (1, "لم يتم الرد"),
        (2, 'العميل موافق علي التكلفة'),
        (3, 'العميل يرفض التكلفة')
    )
    maintenance_type_choices = (
        (1, 'صيانة'),
        (2, 'ضمان')
    )
    date = models.DateTimeField(default=now, verbose_name='تاريخ فتح التذكرة')
    customer = models.ForeignKey(Customer, verbose_name='العميل', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='المنتج', on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='موجه إلي')
    sn = models.CharField(max_length=128, verbose_name='السيريال', null=True, blank=True)
    maintenance_type = models.PositiveSmallIntegerField(default=1, verbose_name='نوع الصيانة',
                                                        choices=maintenance_type_choices)
    problem = models.TextField(verbose_name='المشكلة')
    notes = models.TextField(verbose_name='ملاحظات', null=True, blank=True)
    diagnosis = models.TextField(verbose_name='التشخيص')
    cost = models.PositiveIntegerField(verbose_name='التكلفة', null=True, blank=True, default=0)
    status = models.PositiveSmallIntegerField(default=1, choices=status_choices, verbose_name='حالة التذكرة')
    outsource_status = models.PositiveSmallIntegerField(default=1, choices=outsource_status_choices)
    outsource = models.CharField(max_length=128, verbose_name='حولت إلي', null=True, blank=True)
    shipping_company = models.CharField(max_length=128, verbose_name='شركة الشحن', null=True, blank=True)
    shipping_id = models.CharField(max_length=128, verbose_name='بوليصة الشحن', null=True, blank=True)
    shipping_company2 = models.CharField(max_length=128, verbose_name='شركة الشحن', null=True, blank=True)
    shipping_id2 = models.CharField(max_length=128, verbose_name='بوليصة الشحن', null=True, blank=True)
    customer_received = models.BooleanField(default=False, verbose_name='استلام')
    customer_reply = models.PositiveSmallIntegerField(default=0, verbose_name='رد العميل',
                                                      choices=customer_reply_choices)
    reject_reason = models.TextField(null=True, blank=True, verbose_name='سبب رفض الصيانة')
    done = models.BooleanField(default=False, verbose_name='تمت الصيانة؟')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']
        default_permissions = ()
        permissions = (
            ('add_ticket', 'إضافة تذكرة'),
            ('edit_ticket', 'تعديل تذكرة'),
            ('delete_ticket', 'حذف تذكرة'),
            ('access_ticket_menu', 'الدخول على قائمة التذاكر'),
            ('ticket_transfer', 'تحويل التذكرة'),
            ('ticket_outsource_transfer','تحويل التذكرة الى صيانة خارجية'),
            ('ticket_outsource_received','استلام التذكرة من صيانة خارجية'),
            ('maintenance_diagnosis','تشخيص عطل التذكرة'),
            ('maintenance_cost_rating','تقييم تكلفة الإصلاح'),
            ('maintenance_done','إنهاء الصيانة'),
            ('reject_maintenance','رفض الصيانة'),
            ('device_delivery','تسليم الجهاز للعميل'),
            ('download_tickets_data','تنزيل بيانات التذاكر'),
            ('access_maintenance_report','الدخول على تقارير الصيانة'),
        )


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='رقم التذكرة')
    date = models.DateTimeField(default=now, verbose_name='التوقيت')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='الموظف')
    reply = models.TextField(verbose_name='الرد')
    notify_customer = models.BooleanField(default=False, verbose_name='تنبيه العميل؟')

    def __str__(self):
        return self.reply

    class Meta:
        ordering = ['-id']
        default_permissions = ()
        permissions = (
            ('add_ticket_reply', 'إضافة رد تذكرة'),
            ('edit_ticket_reply', 'تعديل رد تذكرة'),
            ('delete_ticket_reply', 'حذف رد تذكرة'),
            ('access_ticket_reply_menu', 'الدخول على قائمة ردود التذاكر'),
        )


class PrintSetting(models.Model):
    location_choices = (
        (1, 'يمين الفاتورة'),
        (2, 'يسار الفاتورة'),
    )
    footer1_location_choices = (
        (1, 'أعلي الإيصال'),
        (2, 'أسفل الإيصال')
    )
    size_choices = (
        (1, 'A4/A5'),
        (2, 'طابعة ريسيت 8سم')
    )
    size = models.IntegerField(choices=size_choices, default=1, verbose_name='حجم الطباعة')
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='اسم الشركة')
    logo = models.ImageField(null=True, blank=True, verbose_name='اللوجو')
    logo_width = models.FloatField(default=100, verbose_name='نسبة عرض اللوجو في الإيصال')
    logo_location = models.IntegerField(choices=location_choices, default=1, verbose_name='موقع اللوجو')
    text_size = models.FloatField(default=12, verbose_name='حجم الخط في الوصل')
    sales_invoice_title = models.CharField(default='إيصال صيانة', max_length=128,
                                           verbose_name="عنوان الإيصال")
    footer1 = models.TextField(null=True, blank=True, verbose_name='النص 1')
    footer2 = models.TextField(null=True, blank=True, verbose_name='النص 2')
    footer1_location = models.IntegerField(choices=footer1_location_choices, default=2, verbose_name='موضع النص 1')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('edit_maintenance_receipt_setting', 'تعديل إعدادات طباعة إيصالات الصيانة'),
        )
