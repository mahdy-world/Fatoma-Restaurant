from .models import ModulesSetting
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist


def expiration_date(request):
    try:
        obj = ModulesSetting.objects.all().first()
        context = {
            'obj': obj,
        }
        if obj:
            license_expiration = obj.expiration
            support_expiration = obj.support_expiration
            host_expiration = obj.host_expiration
            context.update({

                    'license_expiration': license_expiration.isoformat(),
                    'support_expiration': support_expiration.isoformat(),
                    'host_expiration': host_expiration.isoformat(),
                    'today': now().today().date().isoformat(),
            })
        expired = False
        if obj:
            if license_expiration.isoformat() < now().today().date().isoformat():
                expired = True
            if host_expiration.isoformat() < now().today().date().isoformat():
                expired = True
        context.update({
            'expired': expired,
        })
        return context
    except ObjectDoesNotExist:
        return {
            'expired': False,
        }