from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PersonInfo(models.Model):
    user = models.IntegerField(null=False)
    dob = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=100, null=False)

    def __str__(self):
        return str(self.user)