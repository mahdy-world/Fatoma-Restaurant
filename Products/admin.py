from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(GroupedProduct)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(ProductPrices)