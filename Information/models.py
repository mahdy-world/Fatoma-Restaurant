from django.db import models
from ckeditor.fields import RichTextField
from HR.models import Employee
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class InformationCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    employee = models.ManyToManyField(Employee, verbose_name='الموظفين')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_information_category', 'إضافة تصنيف معلومة'),
            ('edit_information_category', 'تعديل تصنيف معلومة'),
            ('delete_information_category', 'حذف تصنيف معلومة'),
            ('view_informations_category_list', 'الدخول على قائمة تصنيفات المعلومات الإدارية'),
        )


class Information(models.Model):
    title = models.CharField(max_length=128, verbose_name='العنوان')
    employee = models.ManyToManyField(Employee, verbose_name='الموظفين')
    content = RichTextUploadingField(blank=True, null=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.title

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_information', 'إضافة معلومة'),
            ('edit_information', 'تعديل معلومة'),
            ('delete_information', 'حذف معلومة'),
            ('view_information', 'عرض بيانات معلومة'),
            ('view_informations_list', 'الدخول على قائمة المعلومات الإدارية'),
            ('download_information_data', 'تحميل بيانات المعلومات الإدارية'),
        )