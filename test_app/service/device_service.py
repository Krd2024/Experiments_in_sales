# from django.db.models import QuerySet
from django.shortcuts import redirect, render
from test_app.config.color_and_price import (
    COLOR_DICT,
    COLOR_DICT_FOR_STATISTIC,
)
from test_app.config.color_and_price import assign_price
from test_app.models import Button, Device, Price
from loguru import logger
from django.core.cache import cache


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
        # logger.info((color, "--- color ---"))
        # logger.info((price, "--- price ---"))

        price_obj = Price.objects.create(device=device, price=price)
        color_obj = Button.objects.create(device=device, color=color)

        data = {"device": token, "color": color_obj.color, "price": price_obj.price}
        # print(data, "--- data in create_device ---")
        cache.set(token, data)

        # logger.debug((f"{cache.get(token)} ✅ Добавлено в кеш"))

        return data
    except Exception as e:
        pass
        # logger.error(f"Ошибка: {e}")


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
    # logger.debug(data)
    return data


def service_add_devices(request, number_of_device) -> None:

    PRICES = {10: 0, 20: 0, 50: 0, 5: 0}
    COLORS = {"red": 0, "green": 0, "blue": 0}

    # if request.method == "POST":
    #     number_of_device = request.POST.get("device_count")
    print(Device.objects.all().delete())
    cache.clear()
    try:
        if number_of_device.isdigit():
            for i in range(1, int(number_of_device) + 1):
                # Создать запись в БД для Device
                create_device(i)

        devices = Device.objects.prefetch_related("button_set", "price_set").all()
        count_devices = len(devices)
        try:
            for device in devices:
                for device_id in device.button_set.all():
                    # logger.info(
                    #     f"❗Тип device_id.price: {type(device_id.color)}, значение: {device_id.color}"
                    # )

                    # Увеличить значение оного из цветов на 1
                    COLORS[COLOR_DICT_FOR_STATISTIC[device_id.color]] += 1

                for device_id in device.price_set.all():
                    # logger.info(
                    #     f"❗Тип device_id.price: {type(device_id.price)}, значение: {device_id.price}"
                    # )
                    PRICES[device_id.price] += 1

        except Exception as e:
            logger.error(f"ERROR-1: {str(e)}")

        logger.info(PRICES)  # Количественное распределение цен
        logger.info(COLORS)  # Количественное распределение цвета
        # Выводим проценты
        print("Всего устройств:", count_devices, "\n---------------------")
        print("РАСПРЕДЕЛЕНИЕ ЦЕНЫ:\n")

        for price, count in PRICES.items():

            PRICES[price] = float(f"{int(count) / int(count_devices) * 100:.2f}")
            print(f"Цена {price}: {int(count) / int(count_devices) * 100:.2f}%")

        print("-" * 50)

        print("РАСПРЕДЕЛЕНИЕ ЦВЕТА ДЛЯ КНОПОК:\n")
        for color, count in COLORS.items():
            COLORS[color] = f"{count / count_devices * 100:.2f}"
            print(f"Цвет {color}: {count / count_devices * 100:.2f}%")

        return {"price": PRICES, "color": COLORS, "count_devices": count_devices}

    except Exception as e:
        logger.error(f"Ошибка: {e}")
