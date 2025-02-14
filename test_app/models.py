from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    pass


class Device(models.Model):
    token = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device {self.token}"


class Button(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    color = models.CharField(max_length=7)  # HEX-код цвета (#FF0000, #00FF00, #0000FF)

    def __str__(self):
        return f"Button {self.color} for Device {self.device.token}"


class Price(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    price = models.IntegerField()  # Цена (10, 20, 50, 5)

    def __str__(self):
        return f"Price {self.price} for Device {self.device.token}"


class DeviceTest(models.Model):
    token = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device {self.token}"


class ButtonTest(models.Model):
    device = models.ForeignKey(DeviceTest, on_delete=models.CASCADE)
    color = models.CharField(max_length=7)  # HEX-код цвета (#FF0000, #00FF00, #0000FF)

    def __str__(self):
        return f"Button {self.color} for Device {self.device.token}"


class PriceTest(models.Model):
    device = models.ForeignKey(DeviceTest, on_delete=models.CASCADE)
    price = models.IntegerField()  # Цена (10, 20, 50, 5)

    def __str__(self):
        return f"Price {self.price} for Device {self.device.token}"
