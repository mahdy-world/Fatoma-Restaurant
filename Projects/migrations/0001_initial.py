# Generated by Django 3.2.3 on 2021-06-02 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Invoices', '0001_initial'),
        ('Calendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم المشروع')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ البدء')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='تاريخ الإنتهاء')),
                ('complete_percent', models.IntegerField(default=0, verbose_name='نسبة الإنجاز')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.customer', verbose_name='العميل')),
                ('invoices', models.ManyToManyField(to='Invoices.Invoice', verbose_name='فواتير المشروع')),
            ],
            options={
                'permissions': (('add_project', 'إضافة مشروع'), ('edit_project', 'تعديل مشروع'), ('delete_project', 'حذف مشروع'), ('view_project', 'عرض بيانات مشروع'), ('view_project_balance', 'عرض رصيد مشروع'), ('view_project_statement', 'كشف حساب مشروع'), ('access_project_menu', 'الدخول علي قائمة المشروعات')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='حالة المشروع')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
            options={
                'permissions': (('add_project_status', 'إضافة حالة مشروع'), ('edit_project_status', 'تعديل حالة مشروع'), ('delete_project_status', 'حذف حالة مشروع'), ('access_project_status_menu', 'الدخول علي قائمة الشركاء')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ProjectResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='التاريخ')),
                ('type', models.IntegerField(choices=[(1, 'فاتورة'), (2, 'زيارة'), (3, 'موعد'), (4, 'مهام'), (5, 'ملف'), (6, 'مكالمة'), (7, 'تغيير حالة')])),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('visible_to_customer', models.BooleanField(default=False, verbose_name='ظهور للعميل')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Invoices.invoice')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project', verbose_name='المشروع')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Calendar.task')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('delete_project_response', 'حذف شريك'),),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Projects.projectstatus', verbose_name='حالة المشروع'),
        ),
    ]
