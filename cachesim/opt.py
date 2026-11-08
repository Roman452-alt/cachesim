from .base import BaseCache


class OPT(BaseCache):
    """Теоретический алгоритм Белади (Optimal). Требует знания полной трассы."""

    def __init__(self, capacity: int, future_trace: list[int] | None = None):
        super().__init__(capacity)
        self.future_trace: list[int] = list(future_trace) if future_trace else []
        self.current_step: int = 0
        self.pages: set[int] = set()

    def access(self, page: int) -> bool:
        if page in self.pages:
            self.hits += 1
            self.current_step += 1
            return True

        self.misses += 1

        if len(self.pages) == self.capacity:
            # Смотрим, когда страницы из кэша встретятся в будущем
            remaining = self.future_trace[self.current_step + 1 :]
            furthest_page = None
            furthest_dist = -1

            for p in self.pages:
                if p not in remaining:
                    furthest_page = p
                    break
                next_use = remaining.index(p)
                if next_use > furthest_dist:
                    furthest_dist = next_use
                    furthest_page = p

            self.pages.remove(furthest_page)

        self.pages.add(page)
        self.current_step += 1
        return False

    def to_list(self) -> list[int]:
        return list(self.pages)