from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    CLIENT = 'client', 'обычный пользователь'
    MODERATOR = 'moderator', 'модератор'


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город')
    role = models.CharField(choices=UserRoles.choices, default=UserRoles.CLIENT, verbose_name='роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
