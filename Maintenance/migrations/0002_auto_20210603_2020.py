# Generated by Django 3.2.3 on 2021-06-03 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'default_permissions': (), 'ordering': ['-id'], 'permissions': (('add_ticket', 'إضافة تذكرة'), ('edit_ticket', 'تعديل تذكرة'), ('delete_ticket', 'حذف تذكرة'), ('access_ticket_menu', 'الدخول على قائمة التذاكر'), ('ticket_transfer', 'تحويل التذكرة'), ('ticket_outsource_transfer', 'تحويل التذكرة الى صيانة خارجية'), ('ticket_outsource_received', 'استلام التذكرة من صيانة خارجية'), ('maintenance_diagnosis', 'تشخيص عطل التذكرة'), ('maintenance_cost_rating', 'تقييم تكلفة الإصلاح'), ('maintenance_done', 'إنهاء الصيانة'), ('reject_maintenance', 'رفض الصيانة'), ('device_delivery', 'تسليم الجهاز للعميل'))},
        ),
        migrations.AlterModelOptions(
            name='ticketreply',
            options={'default_permissions': (), 'ordering': ['-id'], 'permissions': (('add_ticket_reply', 'إضافة رد تذكرة'), ('edit_ticket_reply', 'تعديل رد تذكرة'), ('delete_ticket_reply', 'حذف رد تذكرة'), ('access_ticket_reply_menu', 'الدخول على قائمة ردود التذاكر'))},
        ),
    ]