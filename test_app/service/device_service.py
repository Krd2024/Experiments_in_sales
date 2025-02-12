from django.db.models import QuerySet
from test_app.config.color_and_price import COLOR_DICT, assign_price
from test_app.models import Button, Device, Price
from loguru import logger
from django.core.cache import cache
from django.http import JsonResponse

COLOR_DICT


def get_color_button(token: str) -> object:
    try:
        device = Device.objects.get(token=token)
        button_obj = Button.objects.get(device=device)
        return button_obj
    except Exception as e:
        logger.error(f"Ошибка {e}")


def get_price(token: str) -> object:
    try:
        device = Device.objects.get(token=token)
        price_obj = Price.objects.get(device=device)
        return price_obj
    except Exception as e:
        logger.error(f"Ошибка {e}")


def create_device(token: str) -> object:
    try:
        device = Device.objects.create(token=token)
        # Получить цвет из словаря согласно группе
        color = COLOR_DICT[device.id % len(COLOR_DICT)]
        price = assign_price()
        logger.info((color, "--- color ---"))
        logger.info((price, "--- price ---"))

        price_obj = Price.objects.create(device=device, price=price)
        color_obj = Button.objects.create(device=device, color=color)

        data = {"device": token, "color": color_obj.color, "price": price_obj.price}
        print(data, "--- data in create_device ---")
        cache.set(token, data)

        logger.debug((f"{cache.get(token)} ✅ Добавлено в кеш"))

        return data
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def action_choice_token(token):
    if not Device.objects.filter(token=token).exists():
        return False
        # Получить цвет кнопки и прайс
    data = cache_price(token)
    logger.debug(data)
    return data


def cache_price(token):
    data = cache.get(token)

    if data is None:
        color_obj = get_color_button(token)
        price_obj = get_price(token)
        data = {"device": token, "color": color_obj.color, "price": price_obj.price}
        cache.set(token, data)
    logger.debug(data)
    return data
