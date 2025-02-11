from django.db.models import QuerySet
from test_app.config.color_and_price import COLOR_DICT
from test_app.models import Button, Device
from loguru import logger

COLOR_DICT


def get_color_button(token: str) -> object:
    device = Device.objects.get(token=token)
    return Button.objects.get(device=device)


def create_device(token: str) -> object:
    try:
        device = Device.objects.create(token=token)
        Button.objects.create(device=device, group=device.id % len(COLOR_DICT))
        return get_color_button(token)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
