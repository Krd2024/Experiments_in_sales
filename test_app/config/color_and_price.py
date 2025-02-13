import random

COLOR_DICT = {0: "#FF0000", 1: "#00FF00", 2: "#0000FF"}
COLOR_DICT_FOR_STATISTIC = {"#FF0000": "red", "#00FF00": "green", "#0000FF": "blue"}


# def dict_for_statistics() -> dict:
#     PRICES = {10: 0, 20: 0, 50: 0, 5: 0}
#     COLORS = {"red": 0, "green": 0, "blue": 0}


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
