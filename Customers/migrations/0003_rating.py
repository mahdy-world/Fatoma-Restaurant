# Generated by Django 3.2.3 on 2021-06-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0002_auto_20210603_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
            options={
                'permissions': (('add_customer_rating', 'إضافة تصنيف عملاء'), ('edit_customer_rating', 'تعديل تصنيف عملاء'), ('delete_customer_rating', 'حذف تصنيف عملاء'), ('access_customer_rating_menu', 'الدخول علي قائمة تصنيفات العملاء')),
                'default_permissions': (),
            },
        ),
    ]
