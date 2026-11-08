import pytest
from cachesim.lfu import LFU


def test_lfu_basic_hit_miss():
    """Базовые промахи и попадания с обновлением частоты."""
    cache = LFU(2)
    assert cache.access(1) is False
    assert cache.access(2) is False
    assert cache.access(1) is True   

    assert cache.hits == 1
    assert cache.misses == 2


def test_lfu_evicts_lowest_frequency():
    """Вытесняется страница с наименьшим числом обращений."""
    cache = LFU(2)
    cache.access(1)
    cache.access(1)   

    cache.access(2)   

    # Добавляем 3: вытесниться должна страница 2, так как ее частота 1 < 2
    assert cache.access(3) is False
    assert 1 in cache.to_list()
    assert 3 in cache.to_list()
    assert 2 not in cache.to_list()


def test_lfu_tie_breaker_uses_lru():
    """При равной частоте вытесняется та страница, к которой обращались раньше."""
    cache = LFU(2)
    cache.access(1)  # freq=1, timer=1
    cache.access(2)  # freq=1, timer=2

     
    cache.access(3)
    assert 1 not in cache.to_list()
    assert 2 in cache.to_list()
    assert 3 in cache.to_list()


def test_lfu_capacity_one():
   
    cache = LFU(1)
    assert cache.access(1) is False
    assert cache.access(1) is True
    assert cache.access(2) is False
    assert cache.to_list() == [2]


def test_lfu_invalid_capacity():
     
    with pytest.raises(ValueError):
        LFU(0)