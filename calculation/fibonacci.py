from functools import lru_cache
from datetime import date

today = date.today()


@lru_cache
# по условию задачи нужно вычислить число фибоначчи + 1 день, тк питон считает индексы с 0 добавлять "+1" не нужно
def fibonacci_calc(n=today.day):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_calc(n - 2) + fibonacci_calc(n - 1)


if __name__ == '__main__':
    print(fibonacci_calc())
