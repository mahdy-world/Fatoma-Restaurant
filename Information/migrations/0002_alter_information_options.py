# Generated by Django 3.2.3 on 2021-06-28 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Information', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='information',
            options={'default_permissions': (), 'permissions': (('add_information', 'إضافة معلومة'), ('edit_information', 'تعديل معلومة'), ('delete_information', 'حذف معلومة'), ('view_information', 'عرض بيانات معلومة'), ('view_informations_list', 'الدخول على قائمة المعلومات الإدارية'))},
        ),
    ]
