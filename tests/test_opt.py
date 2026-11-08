import pytest
from cachesim.opt import OPT


def test_opt_manual_trace():
    trace = [1, 2, 3, 1, 4, 2, 5, 1]
    cache = OPT(capacity=3, future_trace=trace)

    for p in trace:
        cache.access(p)

    assert cache.hits == 3
    assert cache.misses == 5
    assert cache.hit_rate == pytest.approx(3 / 8)


def test_opt_evicts_page_never_used_again():
    trace = [1, 2, 3, 1]
    cache = OPT(capacity=2, future_trace=trace)

    cache.access(1)
    cache.access(2)

    assert cache.access(3) is False
    assert 1 in cache.to_list()
    assert 3 in cache.to_list()
    assert 2 not in cache.to_list()


def test_opt_evicts_furthest_page():
     
    trace = [1, 2, 3, 1, 2]
    cache = OPT(capacity=2, future_trace=trace)

    cache.access(1)
    cache.access(2)

    assert cache.access(3) is False
    assert 1 in cache.to_list()
    assert 3 in cache.to_list()
    assert 2 not in cache.to_list()


def test_opt_capacity_one():

    trace = [1, 1, 2, 1]
    cache = OPT(capacity=1, future_trace=trace)

    assert cache.access(1) is False
    assert cache.access(1) is True
    assert cache.access(2) is False
    assert cache.to_list() == [2]


def test_opt_invalid_capacity():
   
    with pytest.raises(ValueError):
        OPT(0)