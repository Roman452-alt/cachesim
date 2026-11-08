from .base import BaseCache


class Clock(BaseCache):
    """Алгоритм замещения страниц Clock (Second Chance)."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.frames: list[int | None] = [None] * capacity
        self.reference_bits: list[int] = [0] * capacity
        self.hand: int = 0  

    def access(self, page: int) -> bool:
        """Обрабатывает обращение к странице.
        
        True — hit, False — miss.
        """
        for i in range(self.capacity):
            if self.frames[i] == page:
                self.reference_bits[i] = 1
                self.hits += 1
                return True
        self.misses += 1

        while True:
        
            if self.frames[self.hand] is None:
                self.frames[self.hand] = page
                self.reference_bits[self.hand] = 1
                self.hand = (self.hand + 1) % self.capacity
                return False

            if self.reference_bits[self.hand] == 1:
                self.reference_bits[self.hand] = 0
                self.hand = (self.hand + 1) % self.capacity
            else:
                self.frames[self.hand] = page
                self.reference_bits[self.hand] = 1
                self.hand = (self.hand + 1) % self.capacity
                return False

    def to_list(self) -> list[int]:
        """Возвращает занятые слоты страниц (для тестов и отладки)."""
        return [p for p in self.frames if p is not None]