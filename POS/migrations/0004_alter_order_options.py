# Generated by Django 3.2.3 on 2021-06-13 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0003_order_payment_method'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'default_permissions': (), 'permissions': (('add_order', 'إضافة طلب'), ('edit_order', 'تعديل طلب'), ('delete_order', 'حذف طلب'), ('view_order', 'عرض بيانات الطلب'), ('close_order', 'إغلاق الطلب'), ('cancel_order', 'إلغاء الطلب'), ('view_open_order', 'عرض الطلبات المفتوحة'), ('view_closed_order', 'عرض الطلبات المنتهية'), ('view_canceled_order', 'عرض الطلبات الملغية'), ('add_order_discount', 'إضافة خصم للطلب'), ('view_order_bill', 'عرض فاتورة الطلب'), ('edit_order_customer', 'تعديل عميل الطلب'), ('edit_order_address', 'تعديل عنوان العميل الطلب'), ('edit_order_floor', 'تعديل الطابق الخاص بالطلب'), ('edit_order_table', 'عرض الطاولة الخاصة بالطلب'), ('assign_orer_to_delivery', 'اسناد الطلب لمندوب التوصيل'))},
        ),
    ]
