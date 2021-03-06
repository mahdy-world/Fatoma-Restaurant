# Generated by Django 3.2.3 on 2021-07-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0016_productitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('position', models.CharField(max_length=128, verbose_name='المسمى الوظيفي')),
                ('image', models.ImageField(upload_to='')),
                ('facebook', models.CharField(blank=True, max_length=128, null=True, verbose_name='حساب الفيس بوك')),
                ('linkdin', models.CharField(blank=True, max_length=128, null=True, verbose_name='حساب لينكد ان')),
                ('twitter', models.CharField(blank=True, max_length=128, null=True, verbose_name='حساب تويتر')),
                ('Instgram', models.CharField(blank=True, max_length=128, null=True, verbose_name='حساب الانستجرام')),
            ],
        ),
    ]
