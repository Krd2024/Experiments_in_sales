import random

COLOR_DICT = {0: "#FF0000", 1: "#00FF00", 2: "#0000FF"}
COLOR_DICT_FOR_STATISTIC = {"#FF0000": "red", "#00FF00": "green", "#0000FF": "blue"}

LIMIT = 20000


def dict_for_statistics() -> tuple[dict[int, int], dict[str, int]]:
    """
    Словари для подсчёта количества устройств со значениями

    Возвращает два словаря:
    - Первый: ключи (цены) — int, значения — int
    - Второй: ключи (цвета) — str, значения — int
    """
    prices = {10: 0, 20: 0, 50: 0, 5: 0}
    colors = {"red": 0, "green": 0, "blue": 0}
    return prices, colors


def assign_price() -> int:
    """Распределение цены"""
    rand_value = random.random() * 100

    if rand_value < 75:
        return 10  # 75% получат цену 10
    elif rand_value < 85:
        return 20  # 10% получат цену 20
    elif rand_value < 90:
        return 50  # 5% получат цену 50
    else:
        return 5  # 10% получат цену 5
