from django.db import models


# Create your models here.
class AppSetting(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    primary_color = models.CharField(max_length=12)
    secondary_color = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class ModulesSetting(models.Model):
    projects_module = models.BooleanField(default=False, verbose_name='المشروعات')
    invoices_module = models.BooleanField(default=False, verbose_name='الفواتير')
    calendar_module = models.BooleanField(default=False, verbose_name='الأجندة')
    maintenance_module = models.BooleanField(default=False, verbose_name='الصيانة')
    pos_module = models.BooleanField(default=False, verbose_name='نقاط البيع')
    website_module = models.BooleanField(default=False, verbose_name='الموقع')
    expiration = models.DateField(verbose_name='تاريخ إنتهاء الترخيص', default='2020-01-01')
    support_expiration = models.DateField(verbose_name='تاريخ إنتهاء الدعم', default='2020-01-01')
    host_expiration = models.DateField(verbose_name='تاريخ إنتهاء الإستضافة', default='2020-01-01')

    def __str__(self):
        return str(self.id)
