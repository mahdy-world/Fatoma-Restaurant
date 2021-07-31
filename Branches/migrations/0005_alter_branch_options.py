# Generated by Django 3.2.3 on 2021-07-06 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Branches', '0004_alter_treasury_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'default_permissions': (), 'permissions': (('add_branch', 'إضافة فرع'), ('edit_branch', 'تعديل فرع'), ('delete_branch', 'حذف فرع'), ('access_branch_menu', 'الدخول علي قائمة الفروع'), ('download_branch_data', 'تنزيل بيانات الفروع'), ('access_product_stock_balance_report', 'الدخول على تقرير رصيد مخزون منتج'), ('access_product_movement_report', 'الدخول على تقرير حركة منتج'), ('access_branch_inventory_report', 'الدخول على تقرير جرد مخزن'), ('access_items_on_demand_report', 'الدخول على تقرير أصناف تحت حد الطلب'), ('access_items_on_critical_balance_report', 'الدخول على تقرير أصناف وصلت للرصيد الحرج'), ('access_stagnant_report', 'الدخول على تقرير الرواكد'))},
        ),
    ]
