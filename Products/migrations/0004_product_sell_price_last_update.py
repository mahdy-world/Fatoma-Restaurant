# Generated by Django 2.2 on 2021-06-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_productprices'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell_price_last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='آخر تحديث للسعر'),
        ),
    ]
