from test_app.config.color_and_price import (
    COLOR_DICT,
    LIMIT,
)
from test_app.config.color_and_price import assign_price
from test_app.models import Button, ButtonTest, Device, DeviceTest, Price, PriceTest
from loguru import logger
from django.core.cache import cache

from test_app.service.create_statistics import statistics


def get_color_button(token: str) -> object:
    """Получает устройство по токену и возвращает объект кнопки для этого устройства"""
    try:
        device = Device.objects.get(token=token)
        button_obj = Button.objects.get(device=device)
        return button_obj
    except Exception as e:
        logger.error(f"Ошибка {e}")


def get_price(token: str) -> object:
    """Получает устройство по токену и возвращает объект цены для этого устройства"""
    try:
        device = Device.objects.get(token=token)
        price_obj = Price.objects.get(device=device)
        return price_obj
    except Exception as e:
        logger.error(f"Ошибка {e}")


def create_device(token: str) -> object:
    """Создаёт устройство при первом обращении к сервису
    Задаёт цвет и цену в зависимости от группы
    """
    try:
        device = Device.objects.create(token=token)

        # Получить цвет из словаря для группы
        color = COLOR_DICT[device.id % len(COLOR_DICT)]

        # Получить цену согласно процетному распределению
        price = assign_price()

        # Создаём объекты цены и цвета для устройства
        price_obj = Price.objects.create(device=device, price=price)
        color_obj = Button.objects.create(device=device, color=color)

        # Создать словарь для кеша
        data = {"device": token, "color": color_obj.color, "price": price_obj.price}

        # Запись в кеш
        cache.set(token, data)

        logger.debug((f"{cache.get(token)} ✅ Добавлено в кеш"))

        return data
        return price_obj, color_obj
    except Exception as e:
        pass
        logger.error(f"Ошибка: {e}")


def action_choice_token(token):
    """
    Проверяет наличие устройства в БД
    Если нет,
    """
    if not Device.objects.filter(token=token).exists():
        data = create_device(token)
        return {"data": data, "message": "✅ < --- Новая запись"}
    # Получить данные из кеша
    # data = cache_price(token)
    return cache_price(token)


def cache_price(token):
    """
    Проверяет наличие данных об устройстве в кеше

    Если данные есть - возвращает
    Если нет -

    """
    data = cache.get(token)

    if data is None:
        # price_obj, color_obj = create_device(token)
        # logger.debug((price_obj, color_obj))
        color_obj = get_color_button(token)
        price_obj = get_price(token)
        data = {"device": token, "color": color_obj.color, "price": price_obj.price}
        cache.set(token, data)
    logger.debug(data)
    return {"data": data, "message": "✅ < --- Данные из кеша"}


def service_add_devices(request, new_count_devices: str) -> dict[str, str]:
    """
    Получает кол-во устройств для теста.

    Создаёт устройства с цветом кнопки и ценой
    При создании делает списки с объектами для массовой всавки

    """

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
                # Создать и добавить в список устройство
                list_devices.append(Device(token=i))

                color = COLOR_DICT[i % len(COLOR_DICT)]
                price = assign_price()
                # Создать и добавить в список цвет кнопки
                list_color.append(Button(device=list_devices[0], color=color))

                # Создать и добавить в список цену
                list_price.append(Price(device=list_devices[0], price=price))
            except Exception as e:  # noqa
                pass

        # Массовая вставка объектов
        DeviceTest.objects.bulk_create(list_devices)
        ButtonTest.objects.bulk_create(list_color)
        PriceTest.objects.bulk_create(list_price)

        # ================================================================================
        # Получить все устройства и связанные с ними цвета кнопок и цены
        devices = DeviceTest.objects.prefetch_related("button_set", "price_set").all()

        # Возвращает сформированную статистику в виде словаря
        return statistics(devices)

    except Exception as e:
        logger.error(f"Ошибка: {e}")


def work_service(request) -> dict[str, str]:
    """
    Для устройств добавленных через API.

    Получает цвет и цену связанные с устройством
    Возвращает сформированную статистику в виде словаря
    """
    # Получить все устройства и связанные с ними цвета кнопок и цены
    devices = Device.objects.prefetch_related("button_set", "price_set").all()

    # Возвращает сформированную статистику в виде словаря
    return statistics(devices)
