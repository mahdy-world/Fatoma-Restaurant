from django.utils.timezone import now

from Auth.models import *
from Customers.models import *


# Create your models here.
class Task(models.Model):
    type_choices = (
        (1, 'خاص'),
        (2, 'عام'),
    )
    created_date = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name='التاريخ', default=now, null=True)
    task_type = models.IntegerField(choices=type_choices, verbose_name='النوع', default=1)
    related_to = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='متعلقة بـ')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='الموظف', blank=True,
                                 related_name='own_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='المنشئ',
                                    related_name='created_tasks')
    comment = models.TextField(null=True, verbose_name='ملاحظات')
    done = models.BooleanField(default=False, verbose_name='تم')
    done_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.comment

    def is_overdue(self):
        if not self.done:
            if self.date:
                if now().date() > self.date:
                    return True

    def is_today(self):
        if not self.done:
            if self.date:
                if now().date() == self.date:
                    return True

    class Meta:
        default_permissions = ()
        permissions = (
            ('add_task', 'إضافة مهمة او موعد'),
            ('edit_task', 'تعديل مهمة  او موعد'),
            ('delete_task', 'حذف مهمة او موعد'),
            ('access_task_menu', 'الدخول على قائمة المهام والمواعيد'),
            ('end_task', 'إنهاء مهمة او موعد'),
            ('transfer_task', 'تحويل مهمة او موعد'),
            ('download_task_data','تنزيل بيانات المهام والمواعيد')
        )


class TaskRespond(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='الموعد')
    created_date = models.DateTimeField(auto_now=True)
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='تم بواسطة')
    comment = models.TextField(null=True, verbose_name='الرد')

    def __str__(self):
        return self.comment
