from django.contrib import admin
from .models import PersonInfo, ProductInfo, Category, Order, FeedBack, Transaction, ContactUs
# Register your models here.

admin.site.register(PersonInfo)
admin.site.register(ProductInfo)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(FeedBack)
admin.site.register(Transaction)
admin.site.register(ContactUs)
