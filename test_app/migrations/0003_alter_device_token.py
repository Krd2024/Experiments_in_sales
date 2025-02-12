# Generated by Django 5.1.6 on 2025-02-12 10:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_device_button_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='token',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.MaxValueValidator(40), django.core.validators.MinValueValidator(1)]),
        ),
    ]
