# Generated by Django 3.2.3 on 2021-06-13 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_product_sell_price_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='refundable',
            field=models.BooleanField(default=False, verbose_name='منتج قابل للإسترداد'),
        ),
    ]
