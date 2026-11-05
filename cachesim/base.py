from abc import ABC, abstractmethod


class BaseCache(ABC):
    """Абстрактный базовый класс для всех алгоритмов замещения страниц."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    @property
    def hit_rate(self) -> float:
        """Доля попаданий (от 0.0 до 1.0)."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    @abstractmethod
    def access(self, page: int) -> bool:
        """Обработка обращения к странице.
        
        True — hit, False — miss.
        Каждый алгоритм (LRU, Clock) реализует этот метод по-своему.
        """
        pass

    @abstractmethod
    def to_list(self) -> list[int]:
        """Возвращает текущие страницы в кэше (для проверок и тестов)."""
        pass