from django.db import models


# Create your models here.
class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.word


class HomePageSlider(models.Model):
    image = models.ImageField(verbose_name='الصورة')
    title = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    description = models.TextField(verbose_name='تعليق', null=True, blank=True)
    url = models.URLField(verbose_name='تحويل إلي', null=True, blank=True)
    disabled = models.BooleanField(default=False, verbose_name='تعطيل')

    def __str__(self):
        return str(self.id)


class Page(models.Model):
    title = models.CharField(max_length=128, verbose_name='اسم الصفحة')
    content = models.TextField(verbose_name='محتوي الصفحة')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='الكلمات الدلالية')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='تحت صفحة')
    add_to_menu = models.BooleanField(default=False, verbose_name='إضافة للقائمة الرئيسية')

    def __str__(self):
        return self.title


class WebsiteSetting(models.Model):
    primary_color = models.CharField(null=True, blank=True, default='#000000', verbose_name='اللون الاساسي',
                                     max_length=7)
    primary_text_color = models.CharField(null=True, blank=True, default='#ffffff',
                                          verbose_name='لون النص في اللون الاساسي', max_length=7)
    title = models.CharField(max_length=128, default='ON-Link', verbose_name="اسم الموقع")
    logo = models.ImageField(null=True, blank=True, verbose_name='الشعار')

    def __str__(self):
        return self.title

##################################################################
class MainPage(models.Model):
    index_title = models.CharField(max_length=128, verbose_name='عنوان الرئيسية', null=True, blank=True)
    index_text = models.TextField( verbose_name='وصف الرئيسية', null=True, blank=True)
    index_img = models.ImageField(null=True, blank=True, verbose_name='صورة الرئيسية')
    about_vedio = models.CharField(max_length=128, verbose_name='لينك فيديو من نحن', null=True, blank=True)
    about_text = models.TextField( verbose_name='وصف من نحن', null=True, blank=True)
    about_statistics_title = models.CharField(max_length=128, verbose_name='عنوان احصائيات من نحن', null=True, blank=True)
    about_statistics_text = models.TextField(verbose_name='وصف احصائيات من نحن', null=True, blank=True)
    service_text = models.TextField(verbose_name='وصف خدماتنا', null=True, blank=True)
    product_text = models.TextField(verbose_name='وصف منتجاتنا', null=True, blank=True)
    team_text = models.TextField(verbose_name='وصف فريقنا', null=True, blank=True)
    call_text = models.TextField(verbose_name='وصف تواصل معنا', null=True, blank=True)
    address = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    email = models.CharField(max_length=128, verbose_name='الإيميل', null=True, blank=True)
    phone = models.CharField(max_length=128, verbose_name='الهاتف', null=True, blank=True)
    map = models.CharField(max_length=200, verbose_name='لينك الخريطة', null=True, blank=True)

class AboutItems(models.Model):
    title = models.CharField(max_length=128, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')

    def __str__(self):
        return self.title

class StatisticsItems(models.Model):
    title = models.CharField(max_length=128, verbose_name='العنوان')
    number = models.IntegerField(verbose_name='الرقم')

    def __str__(self):
        return self.title

class ServiceItems(models.Model):
    title = models.CharField(max_length=128, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')

    def __str__(self):
        return self.title

class ProductItems(models.Model):
    title = models.CharField(max_length=128, verbose_name='العنوان')
    image = models.ImageField()

    def __str__(self):
        return self.title

class TeamItems(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    position = models.CharField(max_length=128, verbose_name='المسمى الوظيفي')
    image = models.ImageField()
    facebook = models.CharField(max_length=128, verbose_name='حساب الفيس بوك', null=True, blank=True)
    linkdin = models.CharField(max_length=128, verbose_name='حساب لينكد ان', null=True, blank=True)
    twitter = models.CharField(max_length=128, verbose_name='حساب تويتر', null=True, blank=True)
    Instgram = models.CharField(max_length=128, verbose_name='حساب الانستجرام', null=True, blank=True)

    def __str__(self):
        return self.name