from django.db import models


# Create your models here.
class BarcodeSetting(models.Model):
    width = models.FloatField(default=5, verbose_name='عرض الملصق بالسنتيمتر')
    height = models.FloatField(default=1, verbose_name='طول الملصق بالسنتيمتر')
    font_size = models.FloatField(default=8, verbose_name='حجم الخط')
    company_name = models.CharField(max_length=32, verbose_name='اسم الشركة', default="الشركة")
    print_company_name = models.BooleanField(default=True, verbose_name='طباعة اسم الشركة')
    print_price = models.BooleanField(default=True, verbose_name='طباعة السعر')
    print_product_name = models.BooleanField(default=True, verbose_name="طباعة اسم المنتج")

    def __str__(self):
        return str(self.id)

    class Meta:
        default_permissions = ()
        permissions = (
            ('edit_barcode_setting', 'تعديل إعدادات الباركود'),
        )