import random

COLOR_DICT = {0: "#FF0000", 1: "#00FF00", 2: "#0000FF"}
COLOR_DICT_FOR_STATISTIC = {"#FF0000": "red", "#00FF00": "green", "#0000FF": "blue"}


def dict_for_statistics() -> dict:
    prices = {10: 0, 20: 0, 50: 0, 5: 0}
    colors = {"red": 0, "green": 0, "blue": 0}
    return prices, colors


def assign_price() -> int:
    rand_value = random.random() * 100

    if rand_value < 75:
        return 10  # 75% получат цену 10
    elif rand_value < 85:
        return 20  # 10% получат цену 20
    elif rand_value < 90:
        return 50  # 5% получат цену 50
    else:
        return 5  # 10% получат цену 5


def get_count_devices_in_color(colors: dict[str, str]) -> dict[str, int]:
    return {
        "color_red": colors["red"],
        "color_green": colors["green"],
        "color_blue": colors["blue"],
    }


def get_count_devices_in_price(price: dict[str, str]) -> dict[str, int]:
    return {
        10: price[10],
        20: price[20],
        50: price[50],
        5: price[5],
    }
