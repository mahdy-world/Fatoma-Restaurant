# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Branches', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treasury',
            options={'default_permissions': (), 'permissions': (('add_treasury', 'إضافة خزينة و حساب بنكي'), ('edit_treasury', 'تعديل خزينة و حساب بنكي'), ('delete_treasury', 'حذف خزينة و حساب بنكي'), ('access_treasury_menu', 'الدخول علي قائمة الخزائن والحسابات البنكية'))},
        ),
    ]
