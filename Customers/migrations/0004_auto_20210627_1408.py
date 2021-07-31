# Generated by Django 3.2.3 on 2021-06-27 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0003_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rating',
            new_name='Group',
        ),
        migrations.AddField(
            model_name='customer',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customers.group', verbose_name='التصنيف'),
        ),
    ]