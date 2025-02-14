# from django.db.models import QuerySet
from django.shortcuts import redirect, render
from test_app.config.color_and_price import (
    COLOR_DICT,
    COLOR_DICT_FOR_STATISTIC,
    LIMIT,
    dict_for_statistics,
    get_count_devices_in_color,
    get_count_devices_in_price,
)
from test_app.config.color_and_price import assign_price
from test_app.models import Button, ButtonTest, Device, DeviceTest, Price, PriceTest
from loguru import logger
from django.core.cache import cache

from test_app.service.create_statistics import statistics


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

        # Получить цену согласно процетному распределению
        price = assign_price()

        price_obj = Price.objects.create(device=device, price=price)
        color_obj = Button.objects.create(device=device, color=color)

        data = {"device": token, "color": color_obj.color, "price": price_obj.price}
        cache.set(token, data)

        logger.debug((f"{cache.get(token)} ✅ Добавлено в кеш"))

        return data
    except Exception as e:
        pass
        logger.error(f"Ошибка: {e}")


def action_choice_token(token):
    if not Device.objects.filter(token=token).exists():
        return False
        # Получить цвет кнопки и прайс
    data = cache_price(token)
    # logger.debug(data)
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


def service_add_devices(request, new_count_devices: str) -> dict[str, str]:

    if int(new_count_devices) < 0:
        return "Значение меньше нуля"
    if int(new_count_devices) > LIMIT:
        return {"error": f"Больше {LIMIT} не надо"}

    DeviceTest.objects.all().delete()
    try:
        count_devices = int(new_count_devices)

        list_devices = []
        list_color = []
        list_price = []

        for i in range(count_devices):
            try:
                list_devices.append(Device(token=i))

                color = COLOR_DICT[i % len(COLOR_DICT)]
                price = assign_price()

                list_color.append(Button(device=list_devices[0], color=color))
                list_price.append(Price(device=list_devices[0], price=price))
            except Exception as e:  # noqa
                pass

        # Массовая всатвка объектов
        DeviceTest.objects.bulk_create(list_devices)
        ButtonTest.objects.bulk_create(list_color)
        PriceTest.objects.bulk_create(list_price)

        # ================================================================================

        devices = DeviceTest.objects.prefetch_related("button_set", "price_set").all()

        return statistics(devices)

    except Exception as e:
        logger.error(f"Ошибка: {e}")


def work_service(request) -> dict[str, str]:
    devices = devices = Device.objects.prefetch_related("button_set", "price_set").all()
    return statistics(devices)
