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

    prices, colors = dict_for_statistics()

    devices = Device.objects.prefetch_related("button_set", "price_set").all()

    try:

        count_devices = int(new_count_devices)

        Device.objects.all().delete()
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
            except Exception as e:
                pass
        Device.objects.bulk_create(list_devices)
        Button.objects.bulk_create(list_color)
        Price.objects.bulk_create(list_price)

        # ================================================================================

        devices = Device.objects.prefetch_related("button_set", "price_set").all()

        try:
            for device in devices:
                for device_id in device.button_set.all():
                    # Посчитать количество устроойств для каждой группы цвета
                    colors[COLOR_DICT_FOR_STATISTIC[device_id.color]] += 1

                for device_id in device.price_set.all():
                    # Посчитать количество устроойств для каждой группы цен
                    prices[device_id.price] += 1

            # Объеденить в один словарь
            count_devices_dict = {**colors, **prices}

        except Exception as e:
            logger.error(f"ERROR-1: {str(e)}")
            return f"{e}"

        logger.info(prices)  # Количественное распределение цен
        logger.info(colors)  # Количественное распределение цвета

        for price, count in prices.items():
            #
            prices[price] = f"{count / count_devices * 100:.2f}"

        for color, count in colors.items():

            colors[color] = f"{count / count_devices * 100:.2f}"

        return {
            "count_devices_dict": count_devices_dict,
            "price": prices,
            "color": colors,
            "count_devices_now": count_devices,
        }

    except Exception as e:
        logger.error(f"Ошибка: {e}")
