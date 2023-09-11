from django.contrib import admin
from .models import PersonInfo, ProductInfo
# Register your models here.

admin.site.register(PersonInfo)
admin.site.register(ProductInfo)