# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectstatus',
            options={'default_permissions': (), 'permissions': (('add_project_status', 'إضافة حالة مشروع'), ('edit_project_status', 'تعديل حالة مشروع'), ('delete_project_status', 'حذف حالة مشروع'), ('access_project_status_menu', 'الدخول علي قائمة حالات المشاريع'))},
        ),
    ]