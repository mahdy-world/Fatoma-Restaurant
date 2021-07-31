from django.db import models
from Auth.models import User


# Create your models here.
class JobTitle(models.Model):
    name = models.CharField(max_length=128, verbose_name='المسمي الوظيفي')
    description = models.TextField(null=True, blank=True, verbose_name='المهام الوظيفية')
    available_job = models.BooleanField(default=False, verbose_name='توجد وظائف متاحة؟')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name
    
    class Meta:
        default_permissions = ()
        permissions = (
            ('add_job_title', 'إضافة مسمى وظيفي'),
            ('edit_job_title', 'تعديل مسمى وظيفي'),
            ('delete_job_title', 'حذف مسمى وظيفي'),
            ('view_job_title', 'عرض قائمة المسميات الوظيفية'),
            ('download_job_title_data', 'تنزيل بيانات المسميات الوظيفية'),
        )


class Employee(models.Model):
    id_types = (
        (1, 'بطاقة رقم قومي'),
        (2, 'جواز سفر'),
    )
    religion_choices = (
        (1, 'مسلم'),
        (2, 'مسيحي'),
        (3, 'يهودي'),
    )
    social_state_choices = (
        (1, 'أعزب'),
        (2, 'خاطب'),
        (3, 'متزوج'),
        (4, 'مطلق'),
        (5, 'أرمل')
    )
    military_state_choices = (
        (1, 'معفي نهائي'),
        (2, 'معفي مؤقت'),
        (3, 'أتم فترة التجنيد'),
    )
    employee_types = (
        (1, 'متقدم لوظيفة'),
        (2, 'موظف مؤقت'),
        (3, 'موظف دائم'),
    )
    name = models.CharField(max_length=1024, verbose_name='الاسم بالكامل')
    image = models.ImageField(null=True, blank=True, verbose_name='الصورة الشخصية')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='الهاتف')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='العنوان')
    birthday = models.DateField(null=True, blank=True, verbose_name='تاريخ الميلاد')
    email = models.EmailField(null=True, blank=True, verbose_name='البريد الالكتروني')
    qualification = models.CharField(max_length=128, null=True, blank=True, verbose_name='المؤهل')
    id_type = models.IntegerField(choices=id_types, null=True, blank=True, verbose_name='نوع تحقيق الشخصية')
    national_id = models.CharField(max_length=28, null=True, blank=True, verbose_name='رقم تحقيق الشخصية')
    id_issued_from = models.CharField(max_length=128, null=True, blank=True, verbose_name='جهة إصدار تحقيق الشخصية')
    settlement_end_date = models.DateField(null=True, blank=True, verbose_name='انتهاء الاقامة/تحقيق الشخصية')
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='المسمي الوظيفي')
    salary = models.FloatField(null=True, blank=True, verbose_name='الراتب')
    over = models.FloatField(null=True, blank=True, verbose_name='الحافز')
    insurance_start = models.DateField(null=True, blank=True, verbose_name='تاريخ التأمين')
    insurance_end = models.DateField(null=True, blank=True, verbose_name='تاريخ الانتهاء')
    insurance_cost = models.FloatField(null=True, blank=True, verbose_name='تكلفة التأمينات')
    finger_print_id = models.IntegerField(null=True, blank=True, verbose_name='الرقم علي جهاز البصمة')
    start_date = models.DateField(null=True, blank=True, verbose_name='تاريخ التعيين')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاريخ انتهاء العقد')
    religion = models.IntegerField(choices=religion_choices, null=True, blank=True, verbose_name='الديانة')
    military_state = models.IntegerField(choices=military_state_choices, null=True, blank=True, verbose_name='موقف التجنيد')
    relationship = models.IntegerField(choices=social_state_choices, null=True, blank=True, verbose_name='الحالة الاجتماعية')
    rest_credit = models.IntegerField(null=True, blank=True, verbose_name='رصيد الإجازات')
    weekly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة الاسبوعية')
    monthly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة الشهرية')
    yearly_rest_days = models.IntegerField(null=True, blank=True, verbose_name='أيام الاجازة السنوية')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='حساب البرنامج')
    employee_type = models.IntegerField(choices=employee_types, null=True, blank=True, verbose_name='نوع الموظف')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_employee', 'إضافة موظف'),
            ('edit_employee', 'تعديل موظف'),
            ('delete_employee', 'حذف موظف'),
            ('view_employee', 'عرض قائمة الموظفين'),
            ('add_employee_user', 'إضافة حساب لموظف'),
            ('view_employee_data', 'عرض بيانات الموظف'),
            ('login_as_employee', 'الدخول كموظف'),
            ('add_employee_permission', 'إضافة صلاحيات للموظف'),
            ('show_number_of_sales_per_day','عرض عدد المبيعات لكل يوم'),
            ('show_percentage_of_sales_to_expenses','عرض نسبة المبيعات للمصروفات'),
            ('stock_search','بحث عن مخزون'),
            ('product_search','بحث عن منتج'),
            ('employee_search',' بحث عن عميل / مورد'),
            ('show_open_invoices','عرض الفواتير المفتوحة'),
            ('show_sales_value','عرض مبيعات اليوم'),
            ('show_today_calls','عرض مكالمات اليوم'),
            ('show_number_of_new_clients','عرض عدد العملاء الجدد للشهر'),
            ('show_expenses_value','عرض مصروفات اليوم'),
            ('access_financial_statement_report','الدخول على تقرير القائمة المالية'),
            ('access_profits_losses_report','الدخول على تقرير الأرباح والخسائر'),
            ('show_expenses_report','عرض تقارير المصروفات'),
            ('show_receipts_report','عرض تقارير المقبوضات'),
            ('show_new_clients_report','عرض تقارير العملاء الجدد'),
            ('show_calls_report','عرض تقارير المكالمات'),
            ('download_employee_data','تنزيل بيانات الموظفين'),
            ('show_balance_review_report','عرض تقاير ميزان المراجعة'),
            

        )


class EmployeeFile(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف')
    file = models.FileField(verbose_name='الملف')

    def __str__(self):
        return self.file.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_employee_file', 'إضافة ملف موظف'),
            ('edit_employee_file', 'تعديل ملف موظف'),
            ('delete_employee_file', 'حذف ملف موظف'),
            ('view_employee_file', 'عرض ملفات الموظفين'),
        )




