from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):
    phone = models.CharField(max_length = 50, )
    dob = models.DateField(null=True)
    address = models.TextField(null=True)
    is_seller = models.BooleanField(default = False)
    profile_img = models.ImageField(upload_to='images/', null=True, blank=True)


    def __str__(self) -> str:
        return self.username
