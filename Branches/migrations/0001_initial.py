# Generated by Django 3.2.3 on 2021-06-02 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'فرع'), (2, 'مخزن')], verbose_name='النوع')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='العنوان')),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='التليفون')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('add_branch', 'إضافة فرع'), ('edit_branch', 'تعديل فرع'), ('delete_branch', 'حذف فرع'), ('access_branch_menu', 'الدخول علي قائمة الفروع')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Treasury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'خزينة'), (2, 'حساب بنكي'), (3, 'حساب عهدة'), (4, 'حساب سلف رواتب')], verbose_name='النوع')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('no', models.CharField(blank=True, max_length=128, null=True, verbose_name='رقم الحساب')),
                ('initial_balance', models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
