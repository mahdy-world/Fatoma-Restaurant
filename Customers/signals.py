from .models import *
from django.db.models.signals import post_save, pre_save


def save_customer(sender, instance, **kwargs):
    print('Fck')
    history = CustomerHistory()
    history.added_by = instance.added_by
    history.added_at = instance.added_at
    history.type = 1
    history.customer = instance
    history.save()
    print(history.id)


post_save.connect(save_customer, sender=Customer)

