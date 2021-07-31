# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'default_permissions': (), 'permissions': (('add_employee', 'إضافة موظف'), ('edit_employee', 'تعديل موظف'), ('delete_employee', 'حذف موظف'), ('view_employee', 'عرض قائمة الموظفين'), ('add_employee_user', 'إضافة حساب لموظف'), ('view_employee_data', 'عرض بيانات الموظف'), ('login_as_employee', 'الدخول كموظف'), ('add_employee_permission', 'إضافة صلاحيات للموظف'))},
        ),
        migrations.AlterModelOptions(
            name='employeefile',
            options={'default_permissions': (), 'permissions': (('add_employee_file', 'إضافة ملف موظف'), ('edit_employee_file', 'تعديل ملف موظف'), ('delete_employee_file', 'حذف ملف موظف'), ('view_employee_file', 'عرض ملفات الموظفين'))},
        ),
        migrations.AlterModelOptions(
            name='jobtitle',
            options={'default_permissions': (), 'permissions': (('add_job_title', 'إضافة مسمى وظيفي'), ('edit_job_title', 'تعديل مسمى وظيفي'), ('delete_job_title', 'حذف مسمى وظيفي'), ('view_job_title', 'عرض قائمة المسميات الوظيفية'))},
        ),
    ]