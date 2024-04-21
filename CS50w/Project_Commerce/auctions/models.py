from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, default=1000)
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
