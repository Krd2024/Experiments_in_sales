import random


def get_price():
    rand_value = random.random() * 100

    if rand_value < 75:
        return 10  # 75% получат цену 10
    elif rand_value < 85:
        return 20  # 10% получат цену 20
    elif rand_value < 90:
        return 50  # 5% получат цену 50
    else:
        return 5  # 10% получат цену 5


# Тестируем
prices = {10: 0, 20: 0, 50: 0, 5: 0}
trials = 10

for _ in range(trials):
    price = get_price()
    prices[price] += 1

# Выводим проценты
for price, count in prices.items():
    print(f"Цена {price}: {count / trials * 100:.2f}%")
