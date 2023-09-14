from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class PersonInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    dob = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=100, null=False)

    def __str__(self):
        return str(self.user)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=100, null=False)
    img = models.ImageField(upload_to='category', null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) +", "+ self.category_name

class ProductInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=50, null=False)
    price = models.IntegerField()
    PrepTime = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product')
    availability = models.BooleanField(default=True)
    createdDate = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.name
