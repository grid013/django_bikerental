from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=500, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
      return "{}".format(self.email)