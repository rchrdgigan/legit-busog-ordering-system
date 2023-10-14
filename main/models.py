import os
import random
from urllib import response
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import vonage

# Create your models here.


class PersonInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    dob = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=100, null=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=100, null=False)
    img = models.ImageField(upload_to='category', null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) + ", " + self.category_name


class ProductInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=50, null=False)
    price = models.IntegerField()
    PrepTime = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product')
    availability = models.BooleanField(default=True)
    ratings = models.FloatField(null=True, default=5)
    createdDate = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


def random_string():
    return str(random.randint(10000, 99999))


class Order(models.Model):
    transaction_id = models.CharField(max_length=50, default=random_string)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(
        ProductInfo, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    total_amount = models.IntegerField(null=True)
    date = models.DateTimeField(default=now, null=True)
    is_rated = models.BooleanField(null=True)
    note = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.product)


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    total_amount = models.IntegerField(default=0, null=True)
    order_mode = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    cancel_reason = models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) + " - " + str(self.transaction_id)

    def save(self, *args, **kwargs):
        if self.status == 'Out for Delivery':
            user = User.objects.get(id=self.user.id)
            person = PersonInfo.objects.get(user=user)

            TO_NUMBER = person.contact
            VONAGE_API_KEY = '631d7166'
            VONAGE_API_SECRET = 'pNRkF5jFLffncNIc'
            VONAGE_BRAND_NAME = 'LegitBusog'
            client = vonage.Client(
                key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
            sms = vonage.Sms(client)

            responseData = sms.send_message(
                {
                    "from": VONAGE_BRAND_NAME,
                    "to": TO_NUMBER,
                    "text": "Legit Busog: Your order is out for delivery, please prepare the price amount of your order. Thank you!",
                }
            )
            print(responseData)
        return super().save(*args, **kwargs)


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    message = models.TextField(max_length=500, null=True)
    rating = models.IntegerField(null=True)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) + " - " + str(self.order)


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, name=False)
    email = models.EmailField()
    message = models.CharField(max_length=1000, null=False)
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) + " - " + str(self.date_created)
