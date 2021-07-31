from django.db import models
from django.db.models import Sum
from datetime import date
from Customers.models import Category

# Create your models here.
class MainCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_main_category', 'إضافة تصنيف رئيسي للمنتجات'),
            ('edit_main_category', 'تعديل تصنيف رئيسي للمنتجات'),
            ('delete_main_category', 'حذف تصنيف رئيسي للمنتجات'),
            ('access_main_category_menu', 'الدخول علي التصنيف الرئيسية للمنتجات'),
            ('download_main_category_data', 'تنزيل بيانات التصنيفات الرئيسية للمنتجات'),
        )


class SubCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='المجموعة الرئيسية')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        if self.main_category:
            return self.main_category.name + ' - ' + self.name
        else:
            return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_sub_category', 'إضافة تصنيف فرعي للمنتجات'),
            ('edit_sub_category', 'تعديل تصنيف فرعي للمنتجات'),
            ('delete_sub_category', 'حذف تصنيف فرعي للمنتجات'),
            ('access_sub_category_menu', 'الدخول علي التصنيف الفرعية للمنتجات'),
            ('download_sub_category_data', 'تنزيل بيانات التصنيفات الفرعية للمنتجات'),
        )


class Manufacture(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_manufacture', 'إضافة جهة مصنعة للمنتجات'),
            ('edit_manufacture', 'تعديل جهة مصنعة للمنتجات'),
            ('delete_manufacture', 'حذف جهة مصنعة للمنتجات'),
            ('access_manufacture_menu', 'الدخول علي قائمة الجهات المصنعة'),
            ('download_manufacture_data', 'تنزيل بيانات الجهات المصنعة للمنتجات'),
        )


class Brand(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_brand', 'إضافة براند'),
            ('edit_brand', 'تعديل براند'),
            ('delete_brand', 'حذف براند'),
            ('access_brand_menu', 'الدخول علي قائمة البراندات'),
            ('download_brand_data', 'تنزيل بيانات البراندات'),
        )


class Unit(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_unit', 'إضافة وحدة'),
            ('edit_unit', 'تعديل وحدة'),
            ('delete_unit', 'حذف وحدة'),
            ('access_unit_menu', 'الدخول علي قائمة الوحدات'),
        )

class Tax(models.Model):
    types = (
        (1, 'مبلغ ثابت'),
        (2, 'نسبة'),
    )
    name = models.CharField(max_length=128, verbose_name='اسم الضريبة', null=True)
    type = models.IntegerField(choices=types, default=2, verbose_name='النوع')
    value = models.FloatField(default=0.0, verbose_name='القيمة')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_tax', 'إضافة ضريبة'),
            ('edit_tax', 'تعديل ضريبة'),
            ('delete_tax', 'حذف ضريبة'),
            ('access_tax_menu', 'الدخول علي قائمة الضرائب'),
            ('download_tax_data', 'تنزيل بيانات الضرائب'),
        )


class Product(models.Model):
    types = (
        (1, 'منتج عادي'),
        (2, 'منتج مجمع'),
        (3, 'خدمة'),
    )
    unit = (
        (1, 'طن'),
        (2, 'كيلو'),
        (3, 'جرام'),
        (4, 'متر مكعب'),
        (5, 'سانتي متر مكعب'),
        (6, 'لتر'),
        (7, 'ملي لتر'),
        (8, 'قطعة'),
        (9, 'كرتونة'),
    )
    product_type = models.IntegerField(choices=types, default=1, verbose_name='النوع')
    name = models.CharField(max_length=128, verbose_name='الاسم')
    description = models.TextField(verbose_name='وصف المنتج', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='المجموعة')
    manufacture = models.ForeignKey(Manufacture, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='الجهة المصنعة')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='البراند')
    deleted = models.BooleanField(default=False, verbose_name='مسح')
    purchase_price = models.FloatField(default=0.0, verbose_name='سعر الشراء')
    cost_price = models.FloatField(default=0.0, verbose_name='سعر التكلفة')
    sell_price = models.FloatField(default=0.0, verbose_name='سعر البيع')
    main_unit = models.IntegerField(choices=unit, default=8, verbose_name='الوحدة الرئيسية')
    sub_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الوحدة الفرعية',
                                 related_name='sub_unit')
    sub_sub_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='الوحدة الفرعية2', related_name='sub_sub_unit')
    amount_in_sub_unit = models.FloatField(default=0.0, verbose_name='العدد في الوحدة الفرعية')
    amount_in_sub_sub_unit = models.FloatField(default=0.0, verbose_name='العدد في الوحدة الفرعية2')
    max_sell = models.FloatField(verbose_name='حد الصرف', null=True, blank=True)
    full_stock = models.FloatField(verbose_name='حد الطلب', null=True, blank=True)
    critical_stock = models.FloatField(verbose_name='الرصيد الحرج', default=1)
    image = models.ImageField(null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الضريبة المضافة')
    sell_price_last_update = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث للسعر')
    refundable = models.BooleanField(default=False, verbose_name='منتج قابل للإسترداد')

    def __str__(self):
        return self.name

    def current_stock(self):
        stock_in_invoices = [4, 5, 16]
        stock_out_invoices = [1, 2, 3, 6, 15 ,23]
        stock_in = self.invoiceitem_set.all().filter(invoice__deleted=False, invoice__saved=True,
                                                     item__product_type__in=[1, 2],
                                                     invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('quantity'))
        if stock_in['total'] is None:
            stock_in['total'] = 0
        stock_out = self.invoiceitem_set.all().filter(invoice__deleted=False, invoice__saved=True,
                                                      item__product_type__in=[1, 2],
                                                      invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('quantity'))
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total

    def current_stock_value(self):
        if not self.current_stock() is None:
            return self.cost_price * self.current_stock()
        else:
            return 0

    def branch_stock(self, branch):
        stock_in_invoices = [4, 5, 16, 17]
        stock_out_invoices = [1, 2, 3, 6, 15, 17 ,23]
        stock_in = self.invoiceitem_set.all().filter(invoice__to_branch__id=branch, invoice__deleted=False,
                                                     invoice__saved=True, item__product_type__in=[1, 2],
                                                     invoice__invoice_type__in=stock_in_invoices).aggregate(
            total=Sum('quantity'))
        if stock_in['total'] is None:
            stock_in['total'] = 0
        stock_out = self.invoiceitem_set.all().filter(invoice__from_branch__id=branch, invoice__deleted=False,
                                                      invoice__saved=True, item__product_type__in=[1, 2],
                                                      invoice__invoice_type__in=stock_out_invoices).aggregate(
            total=Sum('quantity'))
        print(stock_out)
        if stock_out['total'] is None:
            stock_out['total'] = 0
        total = stock_in['total'] - stock_out['total']
        return total

    def last_sell_date(self):
        invoice_item_set = self.invoiceitem_set.filter(invoice__invoice_type__in=[1, 2, 3]).order_by('invoice__date')
        if invoice_item_set.count() > 0:
            last_sold_invoice = invoice_item_set.last().invoice.date.date()
        else:
            last_sold_invoice = date.today().replace(year=1, month=1, day=1)
        return last_sold_invoice

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_product', 'إضافة منتج'),
            ('edit_product', 'تعديل منتج'),
            ('delete_product', 'حذف منتج'),
            ('view_purchase_price', 'مشاهدة سعر الشراء'),
            ('view_cost_price', 'مشاهدة سعر التكلفة'),
            ('access_product_menu', 'الدخول علي قائمة المنتجات'),
            ('access_product_detail', 'الدخول علي تفاصيل المنتج'),
            ('print_product_label', 'طباعة ملصقات المنتج'),
            ('download_product_data', 'تنزيل بيانات الأصناف'),
        )


class GroupedProduct(models.Model):
    unit = (
        (1, 'طن'),
        (2, 'كيلو'),
        (3, 'جرام'),
        (4, 'متر مكعب'),
        (5, 'سانتي متر مكعب'),
        (6, 'لتر'),
        (7, 'ملي لتر'),
        (8, 'قطعة'),
        (9, 'كرتونة'),
    )
    grouped_item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج المجمع',
                                     related_name='grouped_item')
    contain = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج', related_name='content')
    quantity = models.FloatField(default=0.0, verbose_name='الكمية')
    unit = models.IntegerField(choices=unit, default=8, verbose_name='الوحدة')

    def __str__(self):
        return self.grouped_item.name
    
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_group_product', 'إضافة مكونات منتج'),
            ('edit_group_product', 'تعديل مكونات منتج'),
            ('delete_group_product', 'حذف مكونات منتج'),
            ('access_group_product_menu', 'الدخول علي قائمة مكونات المنتجات'),
        )

class ProductPrices(models.Model):
    op = (
        (1, '-'),
        (2, '+'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='اسم المنتج')
    customer_segment = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name='الشريحة')
    price = models.FloatField(default=0.0, verbose_name='السعر')
    discount = models.FloatField(default=0.0, verbose_name='نسبة الخصم ')
    opration = models.IntegerField(choices=op, default=1, verbose_name='العملية')
    new_price = models.FloatField(default=0.0, verbose_name='السعر بعد الخصم')
    order = models.IntegerField(default=1, null=True, blank=True, verbose_name='الترتيب')
    last_update = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')
    deleted = models.BooleanField(default=False, verbose_name='مسح')
    inactive = models.BooleanField(default=False, verbose_name='تعطيل الشريحة')

    def __str__(self):
        return self.customer_segment.name

    def calculate_after_discount(self):
        if self.opration == 1:
            self.new_price = self.price - (self.price * self.discount / 100)
        else:
            self.new_price = self.price + (self.price * self.discount / 100)
        self.save()
