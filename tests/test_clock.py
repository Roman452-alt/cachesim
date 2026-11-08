import pytest
from cachesim.clock import Clock


def test_clock_manual_trace():
    """Прогон трассы """
    cache = Clock(3)
    trace = [1, 2, 3, 1, 4, 2, 5, 1]

    for p in trace:
        cache.access(p)

  
    assert cache.hits == 2
    assert cache.misses == 6
    assert cache.hit_rate == pytest.approx(2 / 8)


def test_clock_second_chance_mechanism():
    cache = Clock(2)

    cache.access(1)  
    cache.access(2)
    assert cache.access(1) is True

     
    assert cache.access(3) is False
    assert 2 in cache.to_list()
    assert 1 not in cache.to_list()


def test_clock_capacity_one():
    cache = Clock(1)

    assert cache.access(1) is False
    assert cache.access(1) is True
    assert cache.access(2) is False
    assert cache.to_list() == [2]


def test_clock_invalid_capacity():
    with pytest.raises(ValueError):
        Clock(0)