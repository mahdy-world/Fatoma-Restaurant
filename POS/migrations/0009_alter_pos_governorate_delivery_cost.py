# Generated by Django 3.2.3 on 2021-06-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0008_auto_20210629_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos',
            name='governorate_delivery_cost',
            field=models.FloatField(blank=True, null=True, verbose_name='سعر توصيل المحافظة'),
        ),
    ]
