# Generated by Django 3.2.3 on 2021-06-13 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_product_refundable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='refundable',
        ),
    ]
