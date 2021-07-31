from django.db import models
from HR.models import Employee
from Auth.models import User
from Branches.models import Branch ,Treasury
from django.utils.timezone import datetime
from Products.models import Product
from Customers.models import Customer, Address
from Invoices.models import Invoice
from Partners.models import Partner

class POS(models.Model):
    POS_types = (
        (1, 'مطعم'),
        (2, 'محل'),
        (3, 'خدمة توصيل'),
    )

    name = models.CharField(max_length=128, verbose_name='الاسم')
    type = models.IntegerField(choices=POS_types, null=True, blank=True, verbose_name='النوع')
    warehouse = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='تابع لمخزن')
    employees = models.ManyToManyField(Employee, verbose_name='الموظف')
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True , verbose_name='انشأت بواسطة')
    to_treasury = models.ForeignKey(Treasury, verbose_name='الى خزينة', on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=128, verbose_name='كلمة السر' , null=True, blank=True)
    shift_lock = models.BooleanField(default=False, verbose_name='إنهاء الشيفت يتطلب ادخال كلمة السر')
    service = models.FloatField(default=0, verbose_name='سعر الخدمة')
    country = models.CharField(max_length=150, null=True, blank=True, verbose_name='الدولة')
    country_delivery_cost = models.FloatField(default=0, verbose_name='سعر توصيل الدولة')
    region = models.CharField(max_length=150, null=True, blank=True, verbose_name='الإقليم')
    governorate = models.CharField(max_length=150, null=True, blank=True, verbose_name='المحافظة')
    governorate_delivery_cost = models.FloatField(default=0, verbose_name='سعر توصيل المحافظة')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_pos', 'إضافة نقاط البيع'),
            ('edit_pos', 'تعديل نقاط البيع'),
            ('delete_pos', 'حذف نقاط البيع'),
            ('view_pos', 'عرض نقاط البيع'),
            ('view_pos_detail', 'عرض بيانات نقاط البيع'),
            ('enter_pos', 'الدخول لنقطة البيع'),
            ('download_pos_data', 'تنزيل بيانات نقاط البيع'),
        )

class Shift(models.Model):
    shift_status = (
        (1, 'مغلق'),
        (2, 'مفتوح'),
    )

    pos = models.ForeignKey(POS, on_delete=models.CASCADE, verbose_name='تابع لنقطة', null=True, blank=True,)
    date = models.DateField(default=datetime.now, blank=True, verbose_name='التاريخ')
    start_time = models.TimeField(auto_now_add=True, verbose_name='وقت البداية')
    end_time = models.TimeField(verbose_name='وقت النهاية', blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف')
    cashier_no = models.CharField(max_length=128, verbose_name='رقم الكاشير', blank=True, null=True)
    status = models.IntegerField(choices=shift_status, default=2, verbose_name='حالة الشيفت')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, verbose_name='فاتورة الشيفت')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_shift', 'إضافة شيفت'),
            ('edit_shift', 'تعديل شيفت'),
            ('delete_shift', 'حذف شيفت'),
            ('view_shift', 'عرض بيانات شيفت'),
            ('close_shift', 'إغلاق شيفت'),
            ('view_shift_report', 'عرض تقارير الشيفت'),
            ('view_closed_shift', 'عرض الشيفتات المفتوحة'),
            ('view_open_shift', 'عرض الشيفتات المغلقة'),
        )

class Floor(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='اسم او رقم الدور')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, null=True, blank=True, verbose_name='نقطة البيع')

    def __str__(self):
        return str(self.name)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_floor', 'إضافة طابق'),
            ('edit_floor', 'تعديل طابق'),
            ('delete_floor', 'حذف طابق'),
            ('view_floor', 'عرض بيانات الطابق'),
        )

class Table(models.Model):
    status = (
        (1, 'متاح'),
        (2, 'مشغول'),
        (3, 'محجوز'),
    )
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='رقم  الطاولة')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الدور")
    status = models.IntegerField(choices=status, default=1, verbose_name='الحالة')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_table', 'إضافة طاولة'),
            ('edit_table', 'تعديل طاولة'),
            ('delete_table', 'حذف طاولة'),
            ('view_table', 'عرض بيانات الطاولة'),
        )

class Order(models.Model):
    status = (
        (1, 'مفتوح'),
        (2, 'منتهي'),
        (3, 'ملغي'),
    )
    type = (
        (1, 'نسبة'),
        (2, 'قيمة ثابتة'),
    )
    method = (
        (1, 'كاش'),
        (2, 'فيزا'),
    )
    date = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ و وقت الطلب')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, null=True, blank=True, verbose_name='نقطة البيع')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE ,verbose_name='تابع لشيفت')
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='العميل')
    status = models.IntegerField(choices=status, default=1, verbose_name='حالة الطلب')
    taxes = models.FloatField(default=0.0, verbose_name='الضرائب')
    total = models.FloatField(default=0.0, verbose_name='المبلغ الكلي')
    total_paid = models.FloatField(default=0.0, verbose_name='المبلغ المدفوع')
    payment_method = models.IntegerField(choices=method, default=1, verbose_name='طريقة الدفع')
    discount_type = models.IntegerField(choices=type, default=1, verbose_name='نوع الخصم')
    discount_value = models.FloatField(default=0.0, verbose_name='قيمة الخصم')
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='عنوان العميل')
    delivery_cost = models.FloatField(default=0.0, verbose_name='تكلفة التوصيل')
    delivery_employees = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name='مندوب التوصيل')
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الدور")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الطاولة")
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, verbose_name='الشريك')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_order', 'إضافة طلب'),
            ('edit_order', 'تعديل طلب'),
            ('delete_order', 'حذف طلب'),
            ('view_order', 'عرض بيانات الطلب'),
            ('close_order', 'إغلاق الطلب'),
            ('cancel_order', 'إلغاء الطلب'),
            ('view_open_order', 'عرض الطلبات المفتوحة'),
            ('view_closed_order', 'عرض الطلبات المنتهية'),
            ('view_canceled_order', 'عرض الطلبات الملغية'),
            ('add_order_discount', 'إضافة خصم للطلب'),
            ('view_order_bill', 'عرض فاتورة الطلب'),
            ('edit_order_customer', 'تعديل عميل الطلب'),
            ('edit_order_address', 'تعديل عنوان العميل الطلب'),
            ('edit_order_floor', 'تعديل الطابق الخاص بالطلب'),
            ('edit_order_table', 'عرض الطاولة الخاصة بالطلب'),
            ('assign_order_to_delivery', 'اسناد الطلب لمندوب التوصيل'),

        )

class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name='رقم الطلب')
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,verbose_name='الصنف')
    quantity = models.IntegerField(verbose_name='الكمية')
    price = models.FloatField(default=0.0, verbose_name='السعر')
    dicount = models.FloatField(default=0.0, verbose_name='الخصم')
    taxes = models.FloatField(default=0.0, verbose_name=' الضرائب')
    total_wo_taxes = models.FloatField(default=0.0, verbose_name='الكلي بدون ضرائب')
    sub_total = models.FloatField(default=0.0, verbose_name='المبلغ الكلي')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_order_detail', 'إضافة منتجات الطلب'),
            ('edit_order_detail', 'تعديل منتجات الطلب'),
            ('delete_order_detail', 'حذف منتجات الطلب'),
            ('view_order_detail', 'عرض بيانات منتجات الطلب'),
            ('add_order_detail_returns', 'إضافة مرتجعات'),
        )

class OrderPrintSetting(models.Model):
    location_choices = (
        (1, 'يمين الفاتورة'),
        (2, 'يسار الفاتورة'),
    )
    footer1_location_choices = (
        (1, 'أعلي الفاتورة'),
        (2, 'أسفل الفاتورة')
    )
    size_choices = (
        (1, 'A4/A5'),
        (2, 'طابعة ريسيت 8سم')
    )
    size = models.IntegerField(choices=size_choices, default=1, verbose_name='حجم الطباعة')
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='اسم الشركة')
    logo = models.ImageField(null=True, blank=True, verbose_name='اللوجو')
    logo_width = models.FloatField(default=100, verbose_name='نسبة عرض اللوجو في الفاتورة')
    logo_location = models.IntegerField(choices=location_choices, default=1, verbose_name='موقع اللوجو')
    text_size = models.FloatField(default=12, verbose_name='حجم الخط في الفاتورة')
    title = models.CharField(default='فاتورة طلب', max_length=128,
                                           verbose_name="عنوان الفاتورة")
    print_items_discount = models.BooleanField(default=False, verbose_name='طباعة الخصم بجوار المنتجات')
    print_invoice_comments = models.BooleanField(default=False, verbose_name='طباعة ملاحظات الفاتورة')
    footer1 = models.TextField(null=True, blank=True, verbose_name='النص 1')
    footer1_location = models.IntegerField(choices=footer1_location_choices, default=2, verbose_name='موضع النص 1')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_order_print', 'إضافة إعدادات طباعة تقارير نقاط البيع '),
            ('edit_order_print', 'تعديل إعدادات طباعة تقارير نقاط البيع '),
            ('delete_order_print', 'حذف إعدادات طباعة تقارير نقاط البيع '),
            ('view_order_print', 'عرض بيانات إعدادات طباعة تقارير نقاط البيع'),
        )

class PosBaseSetting(models.Model):
    default_customer_in_sales = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                                  verbose_name="العميل الافتراضي للطلبات")

    def __str__(self):
        return str(self.id)
    
    class Meta:
        default_permissions = ()
        permissions = (
            ('edit_pos_setting', 'تعديل إعدادات نقطة البيع'),
        )