from django.db.models import QuerySet
from loguru import logger

from test_app.config.color_and_price import (
    COLOR_DICT_FOR_STATISTIC,
    dict_for_statistics,
)


def statistics(devices: QuerySet) -> dict[str, str]:
    """
    Принимает QuerySet, из которого формирует статистику.
    Возвращает:
    - Общее кол-во устройств
    - Распределение в процентном соотношении цвета и цены каждой группы
    - Распределение в количественном соотношении цвета и цены каждой группы
    -
    """

    try:
        count_devices = len(devices)
        prices, colors = dict_for_statistics()
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
    try:
        for price, count in prices.items():
            prices[price] = f"{count / count_devices * 100:.2f}"

        for color, count in colors.items():
            colors[color] = f"{count / count_devices * 100:.2f}"
    except ZeroDivisionError:
        count_devices = 0
    print("----------------- 1")
    return {
        "count_devices_dict": count_devices_dict,
        "price": prices,
        "color": colors,
        "total_devices": count_devices,
    }
