# Generated by Django 3.2.3 on 2021-07-13 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0005_rename_about_item4_text_mainpage_about_item3_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item1_text',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item1_title',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item2_text',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item2_title',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item3_text',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='about_item3_title',
        ),
        migrations.AddField(
            model_name='mainpage',
            name='about_statistics_text',
            field=models.TextField(blank=True, null=True, verbose_name='وصف احصائيات من نحن'),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='about_statistics_title',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='عنوان احصائيات من نحن'),
        ),
    ]
