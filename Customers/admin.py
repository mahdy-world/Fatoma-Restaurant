from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerHistory)
admin.site.register(CustomerCall)
admin.site.register(Address)
admin.site.register(CustomerGroup)