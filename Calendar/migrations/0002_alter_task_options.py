# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'default_permissions': (), 'permissions': (('add_task', 'إضافة مهمة او موعد'), ('edit_task', 'تعديل مهمة  او موعد'), ('delete_task', 'حذف مهمة او موعد'), ('access_task_menu', 'الدخول على قائمة المهام والمواعيد'), ('end_task', 'إنهاء مهمة او موعد'), ('transfer_task', 'تحويل مهمة او موعد'))},
        ),
    ]