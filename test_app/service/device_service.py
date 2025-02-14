# from django.db.models import QuerySet
from django.shortcuts import redirect, render
from test_app.config.color_and_price import (
    COLOR_DICT,
    COLOR_DICT_FOR_STATISTIC,
    dict_for_statistics,
    get_count_devices_in_color,
    get_count_devices_in_price,
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


def service_add_devices(request, new_count_devices: str) -> dict[str, str]:
    if int(new_count_devices) < 0:
        return "Значение меньше нуля"
    prices, colors = dict_for_statistics()

    devices = Device.objects.prefetch_related("button_set", "price_set").all()
    count_devices_now = len(devices)

    try:
        if int(new_count_devices) < count_devices_now:
            count_devices = int(new_count_devices)
            devices = devices[:count_devices]
        else:
            count_devices = int(new_count_devices)

            # Если введенное кол-во устройств больше чем устройств в базе
            # дозаписывается разница между значениями
            list_obj_devices = []
            for i in range(count_devices):
                # list_obj_devices.append(Device(token=i))

                # Создать запись в БД для Device
                create_device(i)
            devices = Device.objects.prefetch_related("button_set", "price_set").all()

        try:
            for device in devices:
                for device_id in device.button_set.all():
                    # Увеличить значение оного из цветов на 1
                    colors[COLOR_DICT_FOR_STATISTIC[device_id.color]] += 1

                for device_id in device.price_set.all():
                    # Увеличить значение при подсчёте
                    prices[device_id.price] += 1

            # Получить словарь количественного распределения
            # устройств между цветами
            count_devices_dict = get_count_devices_in_color(colors)
            # Получить словарь количественного распределения
            # устройств между ценами
            # Объеденить два словаря
            count_devices_dict.update(get_count_devices_in_price(prices))

            logger.info(count_devices_dict)
        except Exception as e:
            logger.error(f"ERROR-1: {str(e)}")

        logger.info(prices)  # Количественное распределение цен
        logger.info(colors)  # Количественное распределение цвета
        # Выводим проценты
        print("Всего устройств:", count_devices_now, "\n---------------------")
        print("РАСПРЕДЕЛЕНИЕ ЦЕНЫ:\n")

        for price, count in prices.items():
            #
            prices[price] = f"{count / count_devices * 100:.2f}"
            print(f"Цена {price}: {count / count_devices * 100:.2f}%")

        print("-" * 50)

        print("РАСПРЕДЕЛЕНИЕ ЦВЕТА ДЛЯ КНОПОК:\n")

        for color, count in colors.items():
            #

            colors[color] = f"{count / count_devices * 100:.2f}"
            print(f"Цвет {color}: {count / count_devices * 100:.2f}%")

        return {
            "count_devices_dict": count_devices_dict,
            "price": prices,
            "color": colors,
            "count_devices_now": count_devices,
        }

    except Exception as e:
        logger.error(f"Ошибка: {e}")
