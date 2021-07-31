from django.utils.timezone import now

from Auth.models import *
from Branches.models import *
from Customers.models import *
from Products.models import *
from Partners.models import *


# Create your models here.
class SpendCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم التصنيف')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_spend_category', 'إضافة تصنيف مصروفات'),
            ('edit_spend_category', 'تعديل تصنيف مصروفات'),
            ('delete_spend_category', 'حذف تصنيف مصروفات'),
            ('access_spend_category_menu', 'الدخول علي قائمة تصنيفات المصروفات'),
            ('download_spend_category_data','تنزيل بيانات تصنيفات المصروفات'),
        )

class Invoice(models.Model):
    invoice_choices = (
        (1, 'فاتورة مبيعات'),
        (2, 'فاتورة مبيعات توصيل'),
        (3, 'فاتورة مبيعات موقع'),
        (4, 'فاتورة مرتجع مبيعات'),
        (5, 'فاتورة مشتريات'),
        (6, 'فاتورة مرتجع مشتريات'),
        (7, 'عرض أسعار'),
        (8, 'مصروفات عامة'),
        (9, 'دخل عام'),
        (10, 'حساب جاري الشركاء'),
        (11, 'إذن صرف نقدية'),
        (12, 'إذن قبض نقدية'),
        (13, 'إضافة رأس مال'),
        (14, 'سحب من رأس المال'),
        (15, 'فاتورة تسوية عجز'),
        (16, 'فاتورة تسوية زيادة'),
        (17, 'تحويل مخزون'),
        (19, 'تحويل خزينة'),
        (21, 'قبض سداد'),
        (22, 'صرف سداد'),
        (23, 'فاتورة شيفت'),
        (24, 'قيد يومي')
    )
    date = models.DateTimeField(default=now, verbose_name='التاريخ')
    invoice_type = models.IntegerField(choices=invoice_choices, verbose_name='نوع الفاتورة')
    customer = models.ForeignKey(Customer, null=True, verbose_name='العميل / المورد', on_delete=models.SET_NULL)
    partner = models.ForeignKey(Partner, null=True, verbose_name='الشريك', on_delete=models.SET_NULL, blank=True)
    customer_debit = models.FloatField(default=0.0, verbose_name='له')
    customer_credit = models.FloatField(default=0.0, verbose_name='عليه')
    total = models.FloatField(default=0.0, verbose_name='إجمالي')
    discount = models.FloatField(default=0.0, verbose_name='الخصم')
    after_discount = models.FloatField(default=0.0, verbose_name='بعد الخصم')
    shipping = models.FloatField(default=0.0, verbose_name='تكلفة الشحن')
    overall = models.FloatField(default=0.0, verbose_name='إجمالي')
    creator = models.ForeignKey(User, verbose_name='منشئ الفاتورة', on_delete=models.SET_NULL, null=True)
    from_branch = models.ForeignKey(Branch, verbose_name='من مخزن', on_delete=models.SET_NULL, null=True, related_name='branches_out_transactions')
    to_branch = models.ForeignKey(Branch, verbose_name='إلي مخزن', on_delete=models.SET_NULL, null=True, related_name='branches_in_transactions')
    from_treasury = models.ForeignKey(Treasury, verbose_name='من خزينة', on_delete=models.SET_NULL, null=True, related_name='treasury_out_transactions')
    to_treasury = models.ForeignKey(Treasury, verbose_name='إلي خزينة', on_delete=models.SET_NULL, null=True, related_name='treasury_in_transactions')
    treasury_in = models.FloatField(default=0.0, verbose_name='دخل الخزينة')
    treasury_out = models.FloatField(default=0.0, verbose_name='مصروف من الخزينة')
    spend_category = models.ForeignKey(SpendCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='التصنيف')
    comment = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    internal_comment = models.TextField(null=True, blank=True, verbose_name='ملاحظات داخلية')
    saved = models.BooleanField(default=False, verbose_name='حفظ')
    deleted = models.BooleanField(default=False, verbose_name='حذف')
    cost_profit = models.FloatField(default=0.0)
    purchase_profit = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.get_invoice_type_display()) + str(self.id)

    def save_invoice(self):
        self.calculate_profit()
        self.calculate_user_debit_credit()
        self.calculate_after_discount()
        self.calculate_over_all()

    def calculate(self):
        self.calculate_total()
        self.calculate_after_discount()
        self.calculate_over_all()
        self.calculate_profit()
        self.calculate_user_debit_credit()

    def calculate_user_debit_credit(self):
        invoice = self
        if invoice.invoice_type in [1, 2, 3, 6, 21 ,23]:
            invoice.customer_debit = invoice.treasury_in
            invoice.customer_credit = invoice.overall
        if invoice.invoice_type in [4, 5, 22]:
            invoice.customer_credit = invoice.treasury_out
            invoice.customer_debit = invoice.overall
        invoice.save()

    def calculate_profit(self):
        self.cost_profit = 0
        self.purchase_profit = 0
        for x in self.invoiceitem_set.all():
            self.cost_profit += x.cost_profit
            self.purchase_profit += x.purchase_profit
        #self.cost_profit -= self.discount
        #self.purchase_profit -= self.discount
        self.save()

    def calculate_total(self):
        total = 0
        discount = 0
        after_discount = 0
        for x in self.invoiceitem_set.all():
            total += x.total_price
            discount += x.discount
            after_discount += x.after_discount
        self.total = total
        self.discount = discount
        self.after_discount = after_discount

    def calculate_after_discount(self):
        self.after_discount = self.total - self.discount
        self.save()

    def calculate_over_all(self):
        self.overall = self.after_discount + self.shipping
        self.save()

    def invoice_can_edit(self):
        if self.saved or self.deleted:
            return False
        else:
            return True

    def update_cost_profit(self):
        if self.invoice_type == 5:
            for item in self.invoiceitem_set.all():
                item.item.cost_price = item.unit_price
                item.item.save()
        else:
            return None

    class Meta:
        ordering = ['date']
        default_permissions = ()
        permissions = (
            ('undo_save_invoice', 'إعادة فتح الفواتير'),
            ('add_sales_invoice', 'إضافة فاتورة مبيعات'),
            ('delete_invoice', 'حذف الفواتير'),
            ('permanent_delete_invoices', 'حذف نهائي للفواتير'),
            ('restore_deleted_invoices', 'إستعادة الفواتير المحذوفة'),
            ('access_sales_invoice_menu', 'عرض فواتير المبيعات'),
            ('add_reverse_sales_invoice', 'إضافة فاتورة مرتجع مبيعات'),
            ('access_reverse_sales_invoice_menu', 'عرض فواتير مرتجع المبيعات'),
            ('add_purchase_invoice', 'إضافة فاتورة مشتريات'),
            ('access_purchase_invoice_menu', 'عرض فواتير المشتريات'),
            ('add_reverse_purchase_invoice', 'إضافة فاتورة مرتجع مشتريات'),
            ('access_reverse_purchase_invoice_menu', 'عرض فواتير مرتجع المشتريات'),
            ('access_quotation', 'مشاهدة عروض الاسعار'),
            ('add_quotation', 'إضافة عروض أسعار'),
            ('add_branch_transfer', 'إضافة تحويل مخزن'),
            ('delete_branch_transfer', 'حذف تحويل مخزن'),
            ('access_branch_transfer_menu', 'عرض  تحويل مخزن'),
            ('add_treasury_transfer', 'إضافة تحويل نقدية'),
            ('delete_treasury_transfer', 'حذف تحويل نقدية'),
            ('access_treasury_transfer_menu', 'عرض  تحويل نقدية'),
            ('add_income_invoice', 'إضافة سند قبض نقدية'),
            ('delete_income_invoice', 'حذف سند قبض نقدية'),
            ('access_income_invoice_menu', 'عرض سندات قبض نقدية'),
            ('add_outcome_invoice', 'إضافة سند صرف نقدية'),
            ('delete_outcome_invoice', 'حذف سند صرف نقدية'),
            ('access_outcome_invoice_menu', 'عرض سندات صرف نقدية'),
            ('add_capital', 'إضافة لرأس المال'),
            ('minus_capital', 'سحب من رأس المال'),
            ('add_stock_plus_invoice', 'إضافة فاتورة تسوية زيادة'),
            ('access_stock_plus_invoice', 'عرض فاتورة تسوية زيادة'),
            ('add_stock_minus_invoice', 'إضافة فاتورة تسوية عجز'),
            ('access_stock_minus_invoice', 'عرض فاتورة تسوية عجز'),
            ('access_sales_invoice_report', 'عرض تقارير فواتير المبيعات'),
            ('access_reverse_sales_invoice_report', 'عرض تقارير فواتير المبيعات'),
            ('access_purchase_invoice_report', 'عرض تقارير فواتير المبيعات'),
            ('access_reverse_purchase_invoice_report', 'عرض تقارير فواتير المبيعات'),
            ('access_quotation_report', 'عرض تقارير عروض الاسعار'),
            ('show_profit', 'عرض الارباح'),
            ('edit_invoice_date', 'تعديل التاريخ في الفاتورة'),
            ('invoice_discount', 'عمل خصم علي الفاتورة'),
            ('item_discount', 'عمل خصم علي المنتجات'),
            ('edit_item_unit_price', 'تعديل سعر المنتج في الفاتورة'),
            ('edit_invoice_setting', 'تعديل إعدادات الفواتير'),
            ('edit_invoice_print_setting', 'تعديل إعدادات طباعة الفواتير'),
            ('add_customer_income', 'قبض سداد عميل/مورد'),
            ('add_customer_outcome', 'صرف سداد عميل/مورد'),
            ('search_invoice', 'البحث عن فاتورة'),
            ('add_daily_restrictions', 'إضافة قيد يومي'),
            ('delete_daily_restrictions', 'حذف قيد يومي'),
            ('access_daily_restrictions_menu', 'عرض  القيود اليومية'),
            ('daily_restrictions_report', 'عرض تقرير القيود اليومية')
        )

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name='الفاتورة')
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='المنتج')
    quantity = models.FloatField(default=1.0, verbose_name='الكمية')
    unit_price = models.FloatField(default=0.0, verbose_name='سعر الوحدة')
    total_price = models.FloatField(default=0.0, verbose_name='إجمالي')
    discount = models.FloatField(default=0.0, verbose_name='خصم')
    after_discount = models.FloatField(default=0.0, verbose_name='بعد الخصم')
    comment = models.CharField(max_length=64, null=True, blank=True, verbose_name='ملاحظات')
    cost_profit = models.FloatField(default=0.0)
    purchase_profit = models.FloatField(default=0.0)

    def __str__(self):
        return self.item.name

    def calculate(self):
        self.total_price = self.unit_price * self.quantity
        self.after_discount = self.total_price - self.discount
        self.save()
        self.calculate_profit()
        self.invoice.calculate()

    def calculate_profit(self):
        self.cost_profit = self.after_discount - (self.item.cost_price * self.quantity)
        self.purchase_profit = self.after_discount - (self.item.purchase_price * self.quantity)
        self.save()

    class Meta:
        default_permissions = ()
        permissions = (
            ('delete_item_from_invoice', 'حذف منتج من الفاتورة'),
        )

class InvoiceBaseSetting(models.Model):
    sell_without_stock = models.BooleanField(default=False, verbose_name='السماح بالبيع في حالة عدم وجود مخزون كافي')
    alert_on_critical_storage = models.BooleanField(default=True, verbose_name='تحذير عند الوصول للرصيد الحرج')
    view_profit_in_invoice = models.BooleanField(default=True,
                                                 verbose_name='عرض الربح أثناء عمل الفاتورة (لا يظهر الا لمن يمتلك هذه الخاصية)')
    default_customer_in_sales = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                                  verbose_name="العميل الافتراضي لفاتورة المبيعات")
    update_cost_profit_on_purchase = models.BooleanField(default=True,
                                                         verbose_name='تحديث سعر التكلفة تلقائي عند الشراء')
    alert_on_min_cost_price = models.BooleanField(default=True, verbose_name='تحذير عند البيع بأقل من سعر التكلفة')
    alert_on_min_purchase_price = models.BooleanField(default=True, verbose_name='تحذير عند البيع بأقل من سعر الشراء')

    def __str__(self):
        return str(self.id)

class InvoiceSetting(models.Model):
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
    sales_invoice_title = models.CharField(default='فاتورة مبيعات', max_length=128,
                                           verbose_name="عنوان فاتورة المبيعات")
    print_items_discount = models.BooleanField(default=False, verbose_name='طباعة الخصم بجوار المنتجات')
    print_product_description = models.BooleanField(default=False, verbose_name='طباعة وصف المنتج')
    print_product_comments = models.BooleanField(default=False, verbose_name='طباعة ملاحظات المنتج في الفاتورة')
    print_invoice_comments = models.BooleanField(default=False, verbose_name='طباعة ملاحظات الفاتورة')
    print_account_summary = models.BooleanField(default=False, verbose_name='طباعة ملخص حسابات العميل في الفاتورة')
    footer1 = models.TextField(null=True, blank=True, verbose_name='النص 1')
    footer2 = models.TextField(null=True, blank=True, verbose_name='النص 2')
    footer1_location = models.IntegerField(choices=footer1_location_choices, default=2, verbose_name='موضع النص 1')

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('edit_invoice_setting', 'تعديل إعدادات طباعة الفواتير'),
        )
