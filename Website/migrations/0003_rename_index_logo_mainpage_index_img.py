# Generated by Django 3.2.3 on 2021-07-13 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0002_mainpage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainpage',
            old_name='index_logo',
            new_name='index_img',
        ),
    ]
