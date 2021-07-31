# Generated by Django 3.2.3 on 2021-07-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0008_auto_20210713_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpage',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='العنوان'),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='email',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='الإيميل'),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='phone',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='الهاتف'),
        ),
    ]