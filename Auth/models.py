from django.db import models
from django.contrib.auth.models import AbstractUser
from Branches.models import *
from Setting.models import ModulesSetting
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    avatar = models.ImageField(verbose_name='صورة البروفايل', null=True, blank=True)
    default_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='default_branch',
                                       verbose_name='الفرع الافتراضي')
    default_treasury = models.ForeignKey(Treasury, on_delete=models.SET_NULL, null=True,
                                         related_name='default_treasury', verbose_name="الخزينة الافتراضية")
    allowed_branches = models.ManyToManyField(Branch, blank=True, verbose_name="الفروع المتاحة")
    allowed_treasuries = models.ManyToManyField(Treasury, blank=True, verbose_name='الخزائن المتاحة')

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username

    def get_treasuries(self):
        if self.is_superuser:
            return Treasury.objects.all()
        else:
            return self.allowed_treasuries

    def get_branches(self):
        if self.is_superuser:
            return Branch.objects.all()
        else:
            return self.allowed_branches

    def has_access_to_invoices(self):
        setting = ModulesSetting.objects.all().first()
        if setting.invoices_module == True:
            return True
        else:
            return False

    def has_access_to_calendar(self):
        setting = ModulesSetting.objects.all().first()
        if setting.calendar_module == True:
            return True
        else:
            return False

    def has_access_to_maintenance(self):
        setting = ModulesSetting.objects.all().first()
        if setting.maintenance_module == True:
            return True
        else:
            return False

    def has_access_to_projects(self):
        setting = ModulesSetting.objects.all().first()
        if setting.projects_module == True:
            return True
        else:
            return False

    def has_access_to_website(self):
        setting = ModulesSetting.objects.all().first()
        if setting.website_module == True:
            return True
        else:
            return False

    def has_access_to_pos(self):
        setting = ModulesSetting.objects.all().first()
        if setting.pos_module == True:
            return True
        else:
            return False

    def is_owner(self):
        if self.id == 1:
            return True
        else:
            return False

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_user', 'إضافة موظف'),
            ('edit_user', 'تعديل موظف'),
            ('delete_user', 'حذف موظف'),
            ('view_user', 'عرض بيانات موظف'),
            ('edit_user_permissions', 'تعديل صلاحيات موظف'),
            ('access_user_menu', 'الدخول علي قائمة الموظفين'),
        )


class LastSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='online_users', db_column='user_id')
    last_activity = models.DateTimeField()

    # Update
    # @staticmethod
    # def update_user(user):
    #     LastSeen.objects.create(user=user , last_activity=timezone.now())

    # All user act
    # ive
    @staticmethod
    def get_user_active(time_delta=timedelta(minutes=15)):
        starting_time = timezone.now() - time_delta
        return LastSeen.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')

    # All user offline
    @staticmethod
    def get_user_offline(time_delta=timedelta(minutes=15)):
        starting_time = timezone.now() - time_delta
        return LastSeen.objects.filter(last_activity__lte=starting_time).order_by('-last_activity')
