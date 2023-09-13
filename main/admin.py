from django.contrib import admin
from .models import PersonInfo, ProductInfo, Category
# Register your models here.

admin.site.register(PersonInfo)
admin.site.register(ProductInfo)
admin.site.register(Category)
