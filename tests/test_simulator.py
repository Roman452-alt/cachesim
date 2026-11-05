import pytest
from cachesim.lru import LRU
from cachesim.simulator import SimulationResult, run_simulation


def test_simulation_manual_trace():
    cache = LRU(3)
    trace = [1, 2, 3, 1, 4, 2, 5, 1]

    result = run_simulation(cache, trace)

    assert isinstance(result, SimulationResult)
    assert result.hits == 1
    assert result.misses == 7
    assert result.total == 8
    assert result.hit_rate == pytest.approx(0.125)


def test_simulation_empty_trace():
    cache = LRU(3)
    trace = []

    result = run_simulation(cache, trace)

    assert result.hits == 0
    assert result.misses == 0
    assert result.total == 0
    assert result.hit_rate == 0.0