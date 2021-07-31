# Generated by Django 3.2.3 on 2021-07-06 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Partners', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'default_permissions': (), 'permissions': (('add_partner', 'إضافة شريك'), ('edit_partner', 'تعديل شريك'), ('delete_partner', 'حذف شريك'), ('view_partner', 'عرض بيانات شريك'), ('view_partner_balance', 'عرض رصيد شريك'), ('view_partner_statement', 'كشف حساب شريك'), ('access_partner_menu', 'الدخول علي قائمة الشركاء'), ('download_partner_data', 'تنزيل بيانات الشركاء'))},
        ),
    ]
