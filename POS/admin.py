from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Shift)
admin.site.register(POS)
admin.site.register(Order_detail)
admin.site.register(Floor)
admin.site.register(Table)
admin.site.register(PosBaseSetting)