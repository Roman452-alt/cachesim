from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SimulationResult:
    hits: int
    misses: int

    @property
    def total(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        return self.hits / self.total if self.total > 0 else 0.0


def run_simulation(cache: Any, pages: Iterable[int]) -> SimulationResult:
    """Прогоняет трассу обращений pages через переданный кэш."""
    for page in pages:
        cache.access(page)

    return SimulationResult(hits=cache.hits, misses=cache.misses)