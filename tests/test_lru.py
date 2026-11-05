import pytest
from cachesim.lru import LRU

def test_lru_manual_trace():
    """Эталонная ручная трасса: hits=1, misses=7, финал [1, 5, 2]."""
    cache = LRU(3)
    trace = [1, 2, 3, 1, 4, 2, 5, 1]

    for p in trace:
        cache.access(p)

    assert cache.hits == 1
    assert cache.misses == 7
    assert cache.to_list() == [1, 5, 2]


def test_lru_capacity_one():
    """Кэш размера 1: каждое новое обращение вытесняет предыдущую страницу."""
    cache = LRU(1)

    assert cache.access(1) is False
    assert cache.to_list() == [1]

    assert cache.access(1) is True
    assert cache.to_list() == [1]

    assert cache.access(2) is False
    assert cache.to_list() == [2]

    # Страница 1 была вытеснена
    assert cache.access(1) is False
    assert cache.to_list() == [1]
    assert cache.hits == 1
    assert cache.misses == 3

def test_lru_repeats_hit_no_eviction():
    """Повторные обращения к существующей странице не вызывают вытеснения."""
    cache = LRU(2)

    cache.access(10)
    assert cache.access(10) is True
    assert cache.access(10) is True
    assert cache.access(20) is False

    assert cache.hits == 2
    assert cache.misses == 2
    assert set(cache.to_list()) == {10, 20}


def test_lru_hit_updates_recency():
    """Hit перемещает страницу в голову, спасая её от ближайшего вытеснения."""
    cache = LRU(2)

    cache.access(1)  # head: 1, tail: 1
    cache.access(2)  # head: 2, tail: 1
    assert cache.to_list() == [2, 1]

    # Обращение к 1 делает её самой свежей (головой)
    assert cache.access(1) is True
    assert cache.to_list() == [1, 2]

    # Добавляем 3: вытесниться должна 2 (хвост), а не 1
    assert cache.access(3) is False
    assert cache.to_list() == [3, 1]
    assert 2 not in cache._nodes


def test_lru_evicted_page_removed():
    """Вытесненный узел удаляется и из связного списка, и из хэш-таблицы."""
    cache = LRU(2)

    cache.access(1)
    cache.access(2)
    cache.access(3)  # вытесняет 1

    assert 1 not in cache._nodes
    assert 1 not in cache.to_list()
    assert cache.tail.page == 2
    assert cache.head.page == 3


def test_lru_empty_trace():
    """Без обращений кэш пуст, счётчики равны нулю."""
    cache = LRU(3)

    assert cache.hits == 0
    assert cache.misses == 0
    assert cache.to_list() == []
    assert cache.head is None
    assert cache.tail is None


def test_lru_invalid_capacity():
    """Инициализация кэша с неположительной емкостью должна вызывать ValueError."""
    with pytest.raises(ValueError):
        LRU(0)

    with pytest.raises(ValueError):
        LRU(-3)