"""Генераторы тестовых трасс обращений к страницам.

Трасса — список номеров страниц. Все генераторы детерминированы при заданном seed,
поэтому эксперименты можно повторить.
"""

from __future__ import annotations

import random
from collections.abc import Callable


def sequential(n: int, pages: int) -> list[int]:
    """Последовательный проход 0..pages-1, повторённый до длины n."""
    if n <= 0 or pages <= 0:
        raise ValueError("n и pages должны быть положительными")
    return [i % pages for i in range(n)]


def loop(pages: int, rounds: int) -> list[int]:
    """Циклический обход 0..pages-1 заданное число раз."""
    if pages <= 0 or rounds <= 0:
        raise ValueError("pages и rounds должны быть положительными")
    return list(range(pages)) * rounds


def uniform(n: int, pages: int, seed: int = 42) -> list[int]:
    """Случайные обращения с фиксированным seed."""
    if n <= 0 or pages <= 0:
        raise ValueError("n и pages должны быть положительными")
    rng = random.Random(seed)
    return [rng.randrange(pages) for _ in range(n)]


def zipf(n: int, pages: int, alpha: float = 0.8, seed: int = 42) -> list[int]:
    """Обращения с Zipf-распределением: чем меньше номер страницы, тем чаще она встречается."""
    if n <= 0 or pages <= 0:
        raise ValueError("n и pages должны быть положительными")
    if alpha < 0:
        raise ValueError("alpha должна быть неотрицательной")

    weights = [1.0 / ((rank + 1) ** alpha) for rank in range(pages)]
    rng = random.Random(seed)
    return rng.choices(range(pages), weights=weights, k=n)


def thrash(n: int, cache_size: int, seed: int = 42) -> list[int]:
    """Циклический обход рабочего набора больше кэша: cache_size + 1 страниц."""
    if n <= 0 or cache_size <= 0:
        raise ValueError("n и cache_size должны быть положительными")
    working_set = cache_size + 1
    rng = random.Random(seed)
    # Небольшая вариация порядка, чтобы трасса не была идеально периодической.
    base = list(range(working_set))
    rng.shuffle(base)
    return [base[i % working_set] for i in range(n)]


GENERATORS: dict[str, Callable[..., list[int]]] = {
    "sequential": sequential,
    "loop": loop,
    "uniform": uniform,
    "zipf": zipf,
    "thrash": thrash,
}
