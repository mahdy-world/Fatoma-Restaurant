# Generated by Django 3.2.3 on 2021-07-15 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0009_auto_20210713_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpage',
            name='map',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='لينك الخريطة'),
        ),
    ]
