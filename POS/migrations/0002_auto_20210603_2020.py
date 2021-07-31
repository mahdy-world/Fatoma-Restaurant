# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Branches', '0002_alter_treasury_options'),
        ('Invoices', '0001_initial'),
        ('POS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='اسم او رقم الدور')),
            ],
            options={
                'permissions': (('add_floor', 'إضافة طابق'), ('edit_floor', 'تعديل طابق'), ('delete_floor', 'حذف طابق'), ('view_floor', 'عرض بيانات الطابق')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OrderPrintSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(choices=[(1, 'A4/A5'), (2, 'طابعة ريسيت 8سم')], default=1, verbose_name='حجم الطباعة')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='اسم الشركة')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='اللوجو')),
                ('logo_width', models.FloatField(default=100, verbose_name='نسبة عرض اللوجو في الفاتورة')),
                ('logo_location', models.IntegerField(choices=[(1, 'يمين الفاتورة'), (2, 'يسار الفاتورة')], default=1, verbose_name='موقع اللوجو')),
                ('text_size', models.FloatField(default=12, verbose_name='حجم الخط في الفاتورة')),
                ('title', models.CharField(default='فاتورة طلب', max_length=128, verbose_name='عنوان الفاتورة')),
                ('print_items_discount', models.BooleanField(default=False, verbose_name='طباعة الخصم بجوار المنتجات')),
                ('print_invoice_comments', models.BooleanField(default=False, verbose_name='طباعة ملاحظات الفاتورة')),
                ('footer1', models.TextField(blank=True, null=True, verbose_name='النص 1')),
                ('footer1_location', models.IntegerField(choices=[(1, 'أعلي الفاتورة'), (2, 'أسفل الفاتورة')], default=2, verbose_name='موضع النص 1')),
            ],
            options={
                'permissions': (('add_order_print', 'إضافة إعدادات طباعة تقارير نقاط البيع '), ('edit_order_print', 'تعديل إعدادات طباعة تقارير نقاط البيع '), ('delete_order_print', 'حذف إعدادات طباعة تقارير نقاط البيع '), ('view_order_print', 'عرض بيانات إعدادات طباعة تقارير نقاط البيع')),
                'default_permissions': (),
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'default_permissions': (), 'permissions': (('add_order', 'إضافة طلب'), ('edit_order', 'تعديل طلب'), ('delete_order', 'حذف طلب'), ('view_order', 'عرض بيانات الطلب'), ('close_order', 'إغلاق الطلب'), ('cancel_order', 'إلغاء الطلب'), ('view_open_order', 'عرض الطلبات المفتوحة'), ('view_closed_order', 'عرض الطلبات المنتهية'), ('view_canceled_order', 'عرض الطلبات الملغية'), ('add_order_discount', 'إضافة خصم للطلب'), ('view_order_bill', 'عرض فاتورة الطلب'), ('edit_order_customer', 'تعديل عميل الطلب'), ('edit_order_address', 'تعديل عنوان العميل الطلب'), ('edit_order_floor', 'تعديل الطابق الخاص بالطلب'), ('edit_order_table', 'عرض الطاولة الخاصة بالطلب'))},
        ),
        migrations.AlterModelOptions(
            name='order_detail',
            options={'default_permissions': (), 'permissions': (('add_order_detail', 'إضافة منتجات الطلب'), ('edit_order_detail', 'تعديل منتجات الطلب'), ('delete_order_detail', 'حذف منتجات الطلب'), ('view_order_detail', 'عرض بيانات منتجات الطلب'), ('add_order_detail_returns', 'إضافة مرتجعات'))},
        ),
        migrations.AlterModelOptions(
            name='pos',
            options={'default_permissions': (), 'permissions': (('add_pos', 'إضافة نقاط البيع'), ('edit_pos', 'تعديل نقاط البيع'), ('delete_pos', 'حذف نقاط البيع'), ('view_pos', 'عرض نقاط البيع'), ('view_pos_detail', 'عرض بيانات نقاط البيع'), ('enter_pos', 'الدخول لنقطة البيع'))},
        ),
        migrations.AlterModelOptions(
            name='shift',
            options={'default_permissions': (), 'permissions': (('add_shift', 'إضافة شيفت'), ('edit_shift', 'تعديل شيفت'), ('delete_shift', 'حذف شيفت'), ('view_shift', 'عرض بيانات شيفت'), ('close_shift', 'إغلاق شيفت'), ('view_shift_report', 'عرض تقارير الشيفت'), ('view_closed_shift', 'عرض الشيفتات المفتوحة'), ('view_open_shift', 'عرض الشيفتات المغلقة'))},
        ),
        migrations.AddField(
            model_name='pos',
            name='from_treasury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Branches.treasury', verbose_name='من خزينة'),
        ),
        migrations.AddField(
            model_name='pos',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='كلمة السر'),
        ),
        migrations.AddField(
            model_name='pos',
            name='shift_lock',
            field=models.BooleanField(default=False, verbose_name='إنهاء الشيفت يتطلب ادخال كلمة السر'),
        ),
        migrations.AddField(
            model_name='shift',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Invoices.invoice', verbose_name='فاتورة الشيفت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ و وقت الطلب'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='وقت النهاية'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.TimeField(auto_now_add=True, verbose_name='وقت البداية'),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='رقم  الطاولة')),
                ('status', models.IntegerField(choices=[(1, 'متاح'), (2, 'مشغول'), (3, 'محجوز')], default=1, verbose_name='الحالة')),
                ('floor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.floor', verbose_name='الدور')),
            ],
            options={
                'permissions': (('add_table', 'إضافة طاولة'), ('edit_table', 'تعديل طاولة'), ('delete_table', 'حذف طاولة'), ('view_table', 'عرض بيانات الطاولة')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='floor',
            name='pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.pos', verbose_name='نقطة البيع'),
        ),
        migrations.AddField(
            model_name='order',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.floor', verbose_name='الدور'),
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.table', verbose_name='الطاولة'),
        ),
    ]
