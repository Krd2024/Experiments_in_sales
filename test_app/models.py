from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    pass


class Device(models.Model):
    token = models.CharField(
        max_length=255, unique=True
    )  # Уникальный идентификатор устройства
    created_at = models.DateTimeField(auto_now_add=True)  # Дата первого запроса

    def __str__(self):
        return f"Device {self.token}"


class Button(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)  # Связь с устройством
    group = models.IntegerField()  # Номер группы (0, 1, 2)
    color = models.CharField(max_length=7)  # HEX-код цвета (#FF0000, #00FF00, #0000FF)

    def __str__(self):
        return f"Button {self.color} for Device {self.device.token}"


class Price(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)  # Связь с устройством
    group = models.IntegerField()  # Номер группы (по цене)
    price = models.IntegerField()  # Цена (10, 20, 50, 5)

    def __str__(self):
        return f"Price {self.price} for Device {self.device.token}"
