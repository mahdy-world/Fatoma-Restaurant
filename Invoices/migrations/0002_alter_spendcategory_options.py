# Generated by Django 3.2.3 on 2021-07-06 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spendcategory',
            options={'default_permissions': (), 'permissions': (('add_spend_category', 'إضافة تصنيف مصروفات'), ('edit_spend_category', 'تعديل تصنيف مصروفات'), ('delete_spend_category', 'حذف تصنيف مصروفات'), ('access_spend_category_menu', 'الدخول علي قائمة تصنيفات المصروفات'), ('download_spend_category_data', 'تنزيل بيانات تصنيفات المصروفات'))},
        ),
    ]
