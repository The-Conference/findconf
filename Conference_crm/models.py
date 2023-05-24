from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()





