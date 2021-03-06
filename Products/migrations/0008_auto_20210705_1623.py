# Generated by Django 3.2.3 on 2021-07-05 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_product_refundable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'default_permissions': (), 'permissions': (('add_brand', 'إضافة براند'), ('edit_brand', 'تعديل براند'), ('delete_brand', 'حذف براند'), ('access_brand_menu', 'الدخول علي قائمة البراندات'), ('download_brand_data', 'تنزيل بيانات البراندات'))},
        ),
        migrations.AlterModelOptions(
            name='maincategory',
            options={'default_permissions': (), 'permissions': (('add_main_category', 'إضافة تصنيف رئيسي للمنتجات'), ('edit_main_category', 'تعديل تصنيف رئيسي للمنتجات'), ('delete_main_category', 'حذف تصنيف رئيسي للمنتجات'), ('access_main_category_menu', 'الدخول علي التصنيف الرئيسية للمنتجات'), ('download_main_category_data', 'تنزيل بيانات التصنيفات الرئيسية للمنتجات'))},
        ),
        migrations.AlterModelOptions(
            name='manufacture',
            options={'default_permissions': (), 'permissions': (('add_manufacture', 'إضافة جهة مصنعة للمنتجات'), ('edit_manufacture', 'تعديل جهة مصنعة للمنتجات'), ('delete_manufacture', 'حذف جهة مصنعة للمنتجات'), ('access_manufacture_menu', 'الدخول علي قائمة الجهات المصنعة'), ('download_manufacture_data', 'تنزيل بيانات الجهات المصنعة للمنتجات'))},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'default_permissions': (), 'ordering': ['id'], 'permissions': (('add_product', 'إضافة منتج'), ('edit_product', 'تعديل منتج'), ('delete_product', 'حذف منتج'), ('view_purchase_price', 'مشاهدة سعر الشراء'), ('view_cost_price', 'مشاهدة سعر التكلفة'), ('access_product_menu', 'الدخول علي قائمة المنتجات'), ('access_product_detail', 'الدخول علي تفاصيل المنتج'), ('print_product_label', 'طباعة ملصقات المنتج'), ('download_product_data', 'تنزيل بيانات الأصناف'))},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'default_permissions': (), 'permissions': (('add_sub_category', 'إضافة تصنيف فرعي للمنتجات'), ('edit_sub_category', 'تعديل تصنيف فرعي للمنتجات'), ('delete_sub_category', 'حذف تصنيف فرعي للمنتجات'), ('access_sub_category_menu', 'الدخول علي التصنيف الفرعية للمنتجات'), ('download_sub_category_data', 'تنزيل بيانات التصنيفات الفرعية للمنتجات'))},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'default_permissions': (), 'permissions': (('add_tax', 'إضافة ضريبة'), ('edit_tax', 'تعديل ضريبة'), ('delete_tax', 'حذف ضريبة'), ('access_tax_menu', 'الدخول علي قائمة الضرائب'), ('download_tax_data', 'تنزيل بيانات الضرائب'))},
        ),
    ]
