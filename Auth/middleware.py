import datetime

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import LastSeen, User
from django.utils import timezone


class UpdateLastActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last = LastSeen.objects.filter(user_id=request.user.id).first()

            if last:
                last.last_activity = timezone.now()
                last.save()
            else:
                LastSeen.objects.create(user_id=request.user.id, last_activity=timezone.now())

        response = self.get_response(request)
        return response
