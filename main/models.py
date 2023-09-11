from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class PersonInfo(models.Model):
    user = models.IntegerField(null=False)
    dob = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=100, null=False)

    def __str__(self):
        return str(self.user)


class ProductInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False)
    price = models.IntegerField()
    PrepTime = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product', blank=False)
    availability = models.BooleanField(default=True)
    createdDate = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.name
