# Generated by Django 3.2.3 on 2021-07-01 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0002_auto_20210603_2020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'default_permissions': (), 'permissions': (('add_employee', 'إضافة موظف'), ('edit_employee', 'تعديل موظف'), ('delete_employee', 'حذف موظف'), ('view_employee', 'عرض قائمة الموظفين'), ('add_employee_user', 'إضافة حساب لموظف'), ('view_employee_data', 'عرض بيانات الموظف'), ('login_as_employee', 'الدخول كموظف'), ('add_employee_permission', 'إضافة صلاحيات للموظف'), ('show_number_of_sales_per_day', 'عرض عدد المبيعات لكل يوم'), ('show_percentage_of_sales_to_expenses', 'عرض نسبة المبيعات للمصروفات'), ('stock_search', 'بحث عن مخزون'), ('product_search', 'بحث عن منتج'), ('employee_search', ' بحث عن عميل / مورد'), ('show_open_invoices', 'عرض الفواتير المفتوحة'), ('show_site_orders', 'عرض طلبات الموقع'))},
        ),
    ]
