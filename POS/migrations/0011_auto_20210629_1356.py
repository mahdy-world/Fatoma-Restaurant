# Generated by Django 3.2.3 on 2021-06-29 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0008_auto_20210629_1308'),
        ('HR', '0002_auto_20210603_2020'),
        ('POS', '0010_alter_pos_governorate_delivery_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.address', verbose_name='عنوان العميل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.customer', verbose_name='العميل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_employees',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HR.employee', verbose_name='مندوب التوصيل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='POS.floor', verbose_name='الدور'),
        ),
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='POS.table', verbose_name='الطاولة'),
        ),
    ]
