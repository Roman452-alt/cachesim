from .base import BaseCache


class LFU(BaseCache):
    """Алгоритм замещения Least Frequently Used с LRU-тайбрейкером."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.frequencies: dict[int, int] = {}
        self.last_used: dict[int, int] = {}
        self._timer: int = 0

    def access(self, page: int) -> bool:
        self._timer += 1

        if page in self.frequencies:
            self.hits += 1
            self.frequencies[page] += 1
            self.last_used[page] = self._timer
            return True

        self.misses += 1

        if len(self.frequencies) == self.capacity:
            # Ищем страницу с минимальной частотой; при равенстве — с минимальным last_used
            lfu_page = min(
                self.frequencies.keys(),
                key=lambda p: (self.frequencies[p], self.last_used[p]),
            )
            del self.frequencies[lfu_page]
            del self.last_used[lfu_page]

        self.frequencies[page] = 1
        self.last_used[page] = self._timer
        return False

    def to_list(self) -> list[int]:
        # Сортировка по убыванию частоты для отладки
        return sorted(
            self.frequencies.keys(),
            key=lambda p: (self.frequencies[p], self.last_used[p]),
            reverse=True,
        )