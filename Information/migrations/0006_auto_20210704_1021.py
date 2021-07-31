# Generated by Django 3.2.3 on 2021-07-04 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0004_alter_employee_options'),
        ('Information', '0005_alter_information_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='category',
        ),
        migrations.AddField(
            model_name='information',
            name='employee',
            field=models.ManyToManyField(to='HR.Employee', verbose_name='الموظفين'),
        ),
    ]
